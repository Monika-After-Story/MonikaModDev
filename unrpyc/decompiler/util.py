from __future__ import unicode_literals
import sys
import re
from StringIO import StringIO
from contextlib import contextmanager

class DecompilerBase(object):
    def __init__(self, out_file=None, indentation='    ', printlock=None):
        self.out_file = out_file or sys.stdout
        self.indentation = indentation
        self.skip_indent_until_write = False
        self.printlock = printlock

        self.linenumber = 0

        self.block_stack = []
        self.index_stack = []
        self.blank_line_queue = []

    def dump(self, ast, indent_level=0, linenumber=1, skip_indent_until_write=False):
        """
        Write the decompiled representation of `ast` into the opened file given in the constructor
        """
        self.indent_level = indent_level
        self.linenumber = linenumber
        self.skip_indent_until_write = skip_indent_until_write
        if not isinstance(ast, (tuple, list)):
            ast = [ast]
        self.print_nodes(ast)
        return self.linenumber

    @contextmanager
    def increase_indent(self, amount=1):
        self.indent_level += amount
        try:
            yield
        finally:
            self.indent_level -= amount

    def write(self, string):
        """
        Shorthand method for writing `string` to the file
        """
        string = unicode(string)
        self.linenumber += string.count('\n')
        self.skip_indent_until_write = False
        self.out_file.write(string)

    def write_lines(self, lines):
        """
        Write each line in lines to the file without writing whitespace-only lines
        """
        for line in lines:
            if line == '':
                self.write('\n')
            else:
                self.indent()
                self.write(line)

    def save_state(self):
        """
        Save our current state.
        """
        state = (self.out_file, self.skip_indent_until_write, self.linenumber,
            self.block_stack, self.index_stack, self.indent_level, self.blank_line_queue)
        self.out_file = StringIO()
        return state

    def commit_state(self, state):
        """
        Commit changes since a saved state.
        """
        out_file = state[0]
        out_file.write(self.out_file.getvalue())
        self.out_file = out_file

    def rollback_state(self, state):
        """
        Roll back to a saved state.
        """
        (self.out_file, self.skip_indent_until_write, self.linenumber,
            self.block_stack, self.index_stack, self.indent_level, self.blank_line_queue) = state

    def advance_to_line(self, linenumber):
        # If there was anything that we wanted to do as soon as we found a blank line,
        # try to do it now.
        self.blank_line_queue = filter(lambda m: m(linenumber), self.blank_line_queue)
        if self.linenumber < linenumber:
            # Stop one line short, since the call to indent() will advance the last line.
            # Note that if self.linenumber == linenumber - 1, this will write the empty string.
            # This is to make sure that skip_indent_until_write is cleared in that case.
            self.write("\n" * (linenumber - self.linenumber - 1))

    def do_when_blank_line(self, m):
        """
        Do something the next time we find a blank line. m should be a method that takes one
        parameter (the line we're advancing to), and returns whether or not it needs to run
        again.
        """
        self.blank_line_queue.append(m)

    def indent(self):
        """
        Shorthand method for pushing a newline and indenting to the proper indent level
        Setting skip_indent_until_write causes calls to this method to be ignored until something
        calls the write method
        """
        if not self.skip_indent_until_write:
            self.write('\n' + self.indentation * self.indent_level)

    def print_nodes(self, ast, extra_indent=0):
        # This node is a list of nodes
        # Print every node
        with self.increase_indent(extra_indent):
            self.block_stack.append(ast)
            self.index_stack.append(0)

            for i, node in enumerate(ast):
                self.index_stack[-1] = i
                self.print_node(node)

            self.block_stack.pop()
            self.index_stack.pop()

    @property
    def block(self):
        return self.block_stack[-1]

    @property
    def index(self):
        return self.index_stack[-1]

    @property
    def parent(self):
        if len(self.block_stack) < 2:
            return None
        return self.block_stack[-2][self.index_stack[-2]]

    def write_failure(self, message):
        if self.printlock:
            self.printlock.acquire()
        try:
            print message
        finally:
            if self.printlock:
                self.printlock.release()
        self.indent()
        self.write("pass # <<<COULD NOT DECOMPILE: %s>>>" % message)

    def print_unknown(self, ast):
        # If we encounter a placeholder note, print a warning and insert a placeholder
        self.write_failure("Unknown AST node: %s" % str(type(ast)))

    def print_node(self, ast):
        raise NotImplementedError()

class First(object):
    # An often used pattern is that on the first item
    # of a loop something special has to be done. This class
    # provides an easy object which on the first access
    # will return True, but any subsequent accesses False
    def __init__(self, yes_value=True, no_value=False):
        self.yes_value = yes_value
        self.no_value = no_value
        self.first = True

    def __call__(self):
        if self.first:
            self.first = False
            return self.yes_value
        else:
            return self.no_value

def reconstruct_paraminfo(paraminfo):
    if paraminfo is None:
        return ""

    rv = ["("]

    sep = First("", ", ")
    positional = [i for i in paraminfo.parameters if i[0] in paraminfo.positional]
    nameonly = [i for i in paraminfo.parameters if i not in positional]
    for parameter in positional:
        rv.append(sep())
        rv.append(parameter[0])
        if parameter[1] is not None:
            rv.append("=%s" % parameter[1])
    if paraminfo.extrapos:
        rv.append(sep())
        rv.append("*%s" % paraminfo.extrapos)
    if nameonly:
        if not paraminfo.extrapos:
            rv.append(sep())
            rv.append("*")
        for param in nameonly:
            rv.append(sep())
            rv.append(parameter[0])
            if param[1] is not None:
                rv.append("=%s" % parameter[1])
    if paraminfo.extrakw:
        rv.append(sep())
        rv.append("**%s" % paraminfo.extrakw)

    rv.append(")")

    return "".join(rv)

def reconstruct_arginfo(arginfo):
    if arginfo is None:
        return ""

    rv = ["("]
    sep = First("", ", ")
    for (name, val) in arginfo.arguments:
        rv.append(sep())
        if name is not None:
            rv.append("%s=" % name)
        rv.append(val)
    if arginfo.extrapos:
        rv.append(sep())
        rv.append("*%s" % arginfo.extrapos)
    if arginfo.extrakw:
        rv.append(sep())
        rv.append("**%s" % arginfo.extrakw)
    rv.append(")")

    return "".join(rv)

def string_escape(s): # TODO see if this needs to work like encode_say_string elsewhere
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\n', '\\n')
    s = s.replace('\t', '\\t')
    return s

# keywords used by ren'py's parser
KEYWORDS = set(['$', 'as', 'at', 'behind', 'call', 'expression', 'hide',
                'if', 'in', 'image', 'init', 'jump', 'menu', 'onlayer',
                'python', 'return', 'scene', 'set', 'show', 'with',
                'while', 'zorder', 'transform'])

word_regexp = ur'[a-zA-Z_\u00a0-\ufffd][0-9a-zA-Z_\u00a0-\ufffd]*'

def simple_expression_guard(s):
    # Some things we deal with are supposed to be parsed by
    # ren'py's Lexer.simple_expression but actually cannot
    # be parsed by it. figure out if this is the case
    # a slightly more naive approach woudl be to check
    # for spaces in it and surround it with () if necessary
    # but we're not naive
    s = s.strip()

    if Lexer(s).simple_expression():
        return s
    else:
        return "(%s)" % s

def split_logical_lines(s):
    return Lexer(s).split_logical_lines()

class Lexer(object):
    # special lexer for simple_expressions the ren'py way
    # false negatives aren't dangerous. but false positives are
    def __init__(self, string):
        self.pos = 0
        self.length = len(string)
        self.string = string

    def re(self, regexp):
        # see if regexp matches at self.string[self.pos].
        # if it does, increment self.pos
        if self.length == self.pos:
            return None

        match = re.compile(regexp, re.DOTALL).match(self.string, self.pos)
        if not match:
            return None

        self.pos = match.end()
        return match.group(0)

    def eol(self):
        # eat the next whitespace and check for the end of this simple_expression
        self.re(ur"(\s+|\\\n)+")
        return self.pos >= self.length

    def match(self, regexp):
        # strip whitespace and match regexp
        self.re(ur"(\s+|\\\n)+")
        return self.re(regexp)

    def python_string(self, clear_whitespace=True):
        # parse strings the ren'py way (don't parse docstrings, no b/r in front allowed)
        if clear_whitespace:
            return self.match(ur"""(u?(?P<a>"|').*?(?<=[^\\])(?:\\\\)*(?P=a))""")
        else:
            return self.re(ur"""(u?(?P<a>"|').*?(?<=[^\\])(?:\\\\)*(?P=a))""")


    def container(self):
        # parses something enclosed by [], () or {}'s. keyword something
        containers = {"{": "}", "[": "]", "(": ")"}
        if self.eol():
            return None

        c = self.string[self.pos]
        if c not in containers:
            return None
        self.pos += 1

        c = containers[c]

        while not self.eol():
            if c == self.string[self.pos]:
                self.pos += 1
                return True

            if self.python_string() or self.container():
                continue

            self.pos += 1

        return None

    def number(self):
        # parses a number, float or int (but not forced long)
        return self.match(r'(\+|\-)?(\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?')

    def word(self):
        # parses a word
        return self.match(word_regexp)

    def name(self):
        # parses a word unless it's in KEYWORDS.
        pos = self.pos
        word = self.word()

        if word in KEYWORDS:
            self.pos = pos
            return None

        return word

    def simple_expression(self):
        # test if the start string was a simple expression
        start = self.pos

        # check if there's anything in here acctually
        if self.eol():
            return False

        # parse anything which can be called or have attributes requested
        if not(self.python_string() or
               self.number() or
               self.container() or
               self.name()):
            return False

        while not self.eol():

            # if the previous was followed by a dot, there should be a word after it
            if self.match(r'\.'):
                if not self.name():
                    # ren'py errors here. I just stop caring
                    return False

                continue

            # parses slices, function calls, and postfix {}
            if self.container():
                continue

            break

            # are we at the end of the simple expression?
        return self.eol()

    def split_logical_lines(self):
        # split a sequence in logical lines
        # this behaves similarly to .splitlines() which will ignore
        # a trailing \n
        lines = []

        contained = 0

        startpos = self.pos

        while self.pos < self.length:
            c = self.string[self.pos]

            if c == '\n' and not contained and (not self.pos or self.string[self.pos - 1] != '\\'):
                lines.append(self.string[startpos:self.pos])
                # the '\n' is not included in the emitted line
                self.pos += 1
                startpos = self.pos
                continue

            if c in ('(', '[', '{'):
                contained += 1
                self.pos += 1
                continue

            if c in (')', ']', '}') and contained:
                contained -= 1
                self.pos += 1
                continue

            if c == '#':
                self.re("[^\n]*")
                continue

            if self.python_string(False):
                continue

            self.re(r'\w+| +|.') # consume a word, whitespace or one symbol

        if self.pos != startpos:
            lines.append(self.string[startpos:])
        return lines

# Versions of Ren'Py prior to 6.17 put trailing whitespace on the end of
# simple_expressions. This class attempts to preserve the amount of
# whitespace if possible.
class WordConcatenator(object):
    def __init__(self, needs_space, reorderable=False):
        self.words = []
        self.needs_space = needs_space
        self.reorderable = reorderable

    def append(self, *args):
        self.words.extend(filter(None, args))

    def join(self):
        if not self.words:
            return ''
        if self.reorderable and self.words[-1][-1] == ' ':
            for i in xrange(len(self.words) - 1, -1, -1):
                if self.words[i][-1] != ' ':
                    self.words.append(self.words.pop(i))
                    break
        last_word = self.words[-1]
        self.words = map(lambda x: x[:-1] if x[-1] == ' ' else x, self.words[:-1])
        self.words.append(last_word)
        rv = (' ' if self.needs_space else '') + ' '.join(self.words)
        self.needs_space = rv[-1] != ' '
        return rv

# Dict subclass for aesthetic dispatching. use @Dispatcher(data) to dispatch
class Dispatcher(dict):
    def __call__(self, name):
        def closure(func):
            self[name] = func
            return func
        return closure

# ren'py string handling
def encode_say_string(s):
    """
    Encodes a string in the format used by Ren'Py say statements.
    """

    s = s.replace("\\", "\\\\")
    s = s.replace("\n", "\\n")
    s = s.replace("\"", "\\\"")
    s = re.sub(r'(?<= ) ', '\\ ', s)

    return "\"" + s + "\""

# Adapted from Ren'Py's Say.get_code
def say_get_code(ast, inmenu=False):
    rv = [ ]

    if ast.who:
        rv.append(ast.who)

    if hasattr(ast, 'attributes') and ast.attributes is not None:
        rv.extend(ast.attributes)

    # no dialogue_filter applies to us

    rv.append(encode_say_string(ast.what))

    if not ast.interact and not inmenu:
        rv.append("nointeract")

    if ast.with_:
        rv.append("with")
        rv.append(ast.with_)

    return " ".join(rv)
