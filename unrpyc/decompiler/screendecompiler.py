# Copyright (c) 2014 CensoredUsername
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import unicode_literals

import re
import ast
from operator import itemgetter
from contextlib import contextmanager

from util import DecompilerBase, WordConcatenator, reconstruct_paraminfo, \
                 simple_expression_guard, split_logical_lines, Dispatcher
import codegen

# Main API

def pprint(out_file, ast, indent_level=0, linenumber=1,
           decompile_python=False,
           skip_indent_until_write=False, printlock=None):
    return SLDecompiler(out_file, printlock=printlock,
                 decompile_python=decompile_python).dump(
                     ast, indent_level, linenumber, skip_indent_until_write)

# implementation

class SLDecompiler(DecompilerBase):
    """
    an object which handles the decompilation of renpy screen language 1 screens to a given stream
    """

    # This dictionary is a mapping of string: unbound_method, which is used to determine
    # what method to call for which statement
    dispatch = Dispatcher()

    def __init__(self, out_file=None, decompile_python=False,
                 indentation="    ", printlock=None):
        super(SLDecompiler, self).__init__(out_file, indentation, printlock)
        self.decompile_python = decompile_python
        self.should_advance_to_line = True
        self.is_root = True

    def dump(self, ast, indent_level=0, linenumber=1, skip_indent_until_write=False):
        self.indent_level = indent_level
        self.linenumber = linenumber
        self.skip_indent_until_write = skip_indent_until_write
        self.print_screen(ast)
        return self.linenumber

    def advance_to_line(self, linenumber):
        if self.should_advance_to_line:
            super(SLDecompiler, self).advance_to_line(linenumber)

    def save_state(self):
        return (super(SLDecompiler, self).save_state(),
                self.should_advance_to_line, self.is_root)

    def commit_state(self, state):
        super(SLDecompiler, self).commit_state(state[0])

    def rollback_state(self, state):
        self.should_advance_to_line = state[1]
        self.is_root = state[2]
        super(SLDecompiler, self).rollback_state(state[0])

    def to_source(self, node):
        return codegen.to_source(node, self.indentation, False, True)

    @contextmanager
    def not_root(self):
        # Whenever anything except screen itself prints any child nodes, it
        # should be inside a "with self.not_root()" block. It doesn't matter if
        # you catch more inside of the with block than you need, as long as you
        # don't fall back to calling print_python() from inside it.
        is_root = self.is_root
        self.is_root = False
        try:
            yield
        finally:
            self.is_root = is_root

    # Entry point functions

    def print_screen(self, ast):
        # Here we do the processing of the screen statement, and we
        # switch over to parsing of the python string representation

        # Print the screen statement and create the block
        self.indent()
        self.write("screen %s" % ast.name)
        # If we have parameters, print them.
        if hasattr(ast, "parameters") and ast.parameters:
            self.write(reconstruct_paraminfo(ast.parameters))

        if ast.tag:
            self.write(" tag %s" % ast.tag)

        keywords = {ast.code.location[1]: WordConcatenator(False, True)}
        for key in ('modal', 'zorder', 'variant', 'predict'):
            value = getattr(ast, key)
            # Non-Unicode strings are default values rather than user-supplied
            # values, so we don't need to write them out.
            if isinstance(value, unicode):
                if value.linenumber not in keywords:
                    keywords[value.linenumber] = WordConcatenator(False, True)
                keywords[value.linenumber].append("%s %s" % (key, value))
        keywords = sorted([(k, v.join()) for k, v in keywords.items()],
                          key=itemgetter(0)) # so the first one is right
        if self.decompile_python:
            self.print_keywords_and_nodes(keywords, None, True)
            with self.increase_indent():
                self.indent()
                self.write("python:")
                with self.increase_indent():
                    # The first line is always "_1 = (_name, 0)", which gets included
                    # even if the python: block is the only thing in the screen. Don't
                    # include ours, since if we do, it'll be included twice when
                    # recompiled.
                    self.write_lines(self.to_source(ast.code.source).splitlines()[1:])
        else:
            self.print_keywords_and_nodes(keywords, ast.code.source.body, False)

    def split_nodes_at_headers(self, nodes):
        if not nodes:
            return []
        rv = [nodes[:1]]
        parent_id = self.parse_header(nodes[0])
        if parent_id is None:
            raise Exception(
                "First node passed to split_nodes_at_headers was not a header")
        for i in nodes[1:]:
            if self.parse_header(i) == parent_id:
                rv.append([i])
                header = i
            else:
                rv[-1].append(i)
        return rv

    def print_nodes(self, nodes, extra_indent=0, has_block=False):
        # Print a block of statements, splitting it up on one level.
        # The screen language parser emits lines in the shape _0 = (_0, 0) from which indentation can be revealed.
        # It translates roughly to "id = (parent_id, index_in_parent_children)". When parsing a block
        # parse the first header line to find the parent_id, and then split around headers with the same parent id
        # in this block.
        if has_block and not nodes:
            raise BadHasBlockException()
        split = self.split_nodes_at_headers(nodes)
        with self.increase_indent(extra_indent):
            for i in split:
                self.print_node(i[0], i[1:], has_block)

    def get_first_line(self, nodes):
        if self.get_dispatch_key(nodes[0]):
            return nodes[0].value.lineno
        elif self.is_renpy_for(nodes):
            return nodes[1].target.lineno
        elif self.is_renpy_if(nodes):
            return nodes[0].test.lineno
        else:
            # We should never get here, but just in case...
            return nodes[0].lineno

    def make_printable_keywords(self, keywords, lineno):
        keywords = [(i.arg, simple_expression_guard(self.to_source(i.value)),
            i.value.lineno) for i in keywords if not (isinstance(
            i.value, ast.Name) and (
            (i.arg == 'id' and i.value.id.startswith('_')) or
            (i.arg == 'scope' and i.value.id == '_scope')))]
        # Sort the keywords according to what line they belong on
        # The first element always exists for the line the block starts on,
        # even if there's no keywords that go on it
        keywords_by_line = []
        current_line = []
        for i in keywords:
            if i[2] > lineno:
                keywords_by_line.append((lineno, ' '.join(current_line)))
                lineno = i[2]
                current_line = []
            current_line.extend(i[:2])
        keywords_by_line.append((lineno, ' '.join(current_line)))
        return keywords_by_line

    def print_keywords_and_nodes(self, keywords, nodes, needs_colon):
        # Keywords and child nodes can be mixed with each other, so they need
        # to be printed at the same time. This function takes each list and
        # combines them into one, then prints it.
        #
        # This function assumes line numbers of nodes before keywords are
        # correct, which is the case for the "screen" statement itself.
        if keywords:
            if keywords[0][1]:
                self.write(" %s" % keywords[0][1])
            if len(keywords) != 1:
                needs_colon = True
        if nodes:
            nodelists = [(self.get_first_line(i[1:]), i)
                         for i in self.split_nodes_at_headers(nodes)]
            needs_colon = True
        else:
            nodelists = []
        if needs_colon:
            self.write(":")
        stuff_to_print = sorted(keywords[1:] + nodelists, key=itemgetter(0))
        with self.increase_indent():
            for i in stuff_to_print:
                # Nodes are lists. Keywords are ready-to-print strings.
                if type(i[1]) == list:
                    self.print_node(i[1][0], i[1][1:])
                else:
                    self.advance_to_line(i[0])
                    self.indent()
                    self.write(i[1])

    def get_lines_used_by_node(self, node):
        state = self.save_state()
        self.print_node(node[0], node[1:])
        linenumber = self.linenumber
        self.rollback_state(state)
        return linenumber - self.linenumber

    def print_buggy_keywords_and_nodes(self, keywords, nodes, needs_colon, has_block):
        # Keywords and child nodes can be mixed with each other, so they need
        # to be printed at the same time. This function takes each list and
        # combines them into one, then prints it.
        #
        # This function assumes line numbers of nodes before keywords are
        # incorrect, which is the case for everything except the "screen"
        # statement itself.
        last_keyword_lineno = None
        if keywords:
            if keywords[0][1]:
                self.write(" %s" % keywords[0][1])
            remaining_keywords = keywords[1:]
            if remaining_keywords:
                needs_colon = True
                last_keyword_lineno = remaining_keywords[-1][0]
        if nodes:
            nodelists = [(self.get_first_line(i[1:]), i)
                         for i in self.split_nodes_at_headers(nodes)]
        else:
            nodelists = []
        for key, value in enumerate(nodelists):
            if last_keyword_lineno is None or value[0] > last_keyword_lineno:
                nodes_before_keywords = nodelists[:key]
                nodes_after_keywords = nodelists[key:]
                break
        else:
            nodes_before_keywords = nodelists
            nodes_after_keywords = []
        if nodes_before_keywords or (not has_block and nodes_after_keywords):
            needs_colon = True
        if needs_colon:
            self.write(":")
        with self.increase_indent():
            should_advance_to_line = self.should_advance_to_line
            self.should_advance_to_line = False
            while nodes_before_keywords:
                if not remaining_keywords:
                    # Something went wrong. We already printed the last keyword,
                    # yet there's still nodes left that should have been printed
                    # before the last keyword. Just print them now.
                    for i in nodes_before_keywords:
                        self.print_node(i[1][0], i[1][1:])
                    break
                # subtract 1 line since .indent() uses 1
                lines_to_go = remaining_keywords[0][0] - self.linenumber - 1
                next_node = nodes_before_keywords[0][1]
                if lines_to_go >= self.get_lines_used_by_node(next_node):
                    self.print_node(next_node[0], next_node[1:])
                    nodes_before_keywords.pop(0)
                elif not should_advance_to_line or lines_to_go <= 0:
                    self.indent()
                    self.write(remaining_keywords.pop(0)[1])
                else:
                    self.write("\n" * lines_to_go)
            self.should_advance_to_line = should_advance_to_line
            for i in remaining_keywords:
                self.advance_to_line(i[0])
                self.indent()
                self.write(i[1])
        with self.increase_indent(1 if not has_block else 0):
            for i in nodes_after_keywords:
                self.print_node(i[1][0], i[1][1:])

    def get_dispatch_key(self, node):
        if (isinstance(node, ast.Expr) and
                isinstance(node.value, ast.Call) and
                isinstance(node.value.func, ast.Attribute) and
                isinstance(node.value.func.value, ast.Name)):
            return node.value.func.value.id, node.value.func.attr
        else:
            return None

    def print_node(self, header, code, has_block=False):
        # Here we derermine how to handle a statement.
        # To do this we look at how the first line in the statement code starts, after the header.
        # Then we call the appropriate function as specified in ui_function_dict.
        # If the statement is unknown, we can still emit valid screen code by just
        # stuffing it inside a python block.

        # There's 3 categories of things that we can convert to screencode:
        # if statements, for statements, and function calls of the
        # form "first.second(...)". Anything else gets converted to Python.
        dispatch_key = self.get_dispatch_key(code[0])
        if dispatch_key:
            func = self.dispatch.get(dispatch_key, self.print_python.__func__)
            if has_block:
                if func not in (self.print_onechild.__func__,
                    self.print_manychildren.__func__):
                    raise BadHasBlockException()
                func(self, header, code, True)
            else:
                func(self, header, code)
        elif has_block:
            raise BadHasBlockException()
        elif self.is_renpy_for(code):
            self.print_for(header, code)
        elif self.is_renpy_if(code):
            self.print_if(header, code)
        else:
            self.print_python(header, code)
    # Helper printing functions

    def print_args(self, node):
        if node.args:
            self.write(" " + " ".join([simple_expression_guard(
                self.to_source(i)) for i in node.args]))

    # Node printing functions

    def print_python(self, header, code):
        # This function handles any statement which is a block but couldn't logically be
        # Translated to a screen statement.
        #
        # Ren'Py's line numbers are really, really buggy. Here's a summary:
        # If we're not directly under the root screen, and a keyword for our
        # parent follows us, then all of our line numbers will be equal to the
        # line number of that keyword.
        # If we're not directly under the root screen, and no keywords for our
        # parent follow us, then header.lineno is the line number of whatever
        # it is that preceded us (which is completely useless).
        # If we're directly under the root "screen", then header.lineno is the
        # line that "$" or "python:" appeared on.
        # If we're not a child followed by a keyword, and "$" was used, then
        # code[0].lineno is the line that the code actually starts on, but if
        # "python:" was used, then all of code's line numbers will be 1 greater
        # than the line each one should be.
        source = self.to_source(ast.Module(body=code,
                                           lineno=code[0].lineno,
                                           col_offset=0)).rstrip().lstrip('\n')
        lines = source.splitlines()
        if len(split_logical_lines(source)) == 1 and (
                (not self.is_root and code[0].lineno < self.linenumber + 3) or
                header.lineno >= code[0].lineno):
            # This is only one logical line, so it's possible that it was $,
            # and either it's not in the root (so we don't know what the
            # original source used), or it is in the root and we know it used $.
            # Also, if we don't know for sure what was used, but we have enough
            # room to use a "python" block, then use it instead, since it'll
            # result in everything taking up one fewer line (since it'll use
            # one more, but start two sooner).
            self.advance_to_line(code[0].lineno)
            self.indent()
            self.write("$ %s" % lines[0])
            self.write_lines(lines[1:])
        else:
            # Either this is more than one logical line, so it has to be a
            # python block, or it was in the root and we can tell that it was
            # originally a python block.
            if self.is_root:
                self.advance_to_line(header.lineno)
            self.indent()
            self.write("python:")
            self.advance_to_line(code[0].lineno - 1)
            with self.increase_indent():
                self.write_lines(lines)

    def is_renpy_if(self, nodes):
        return len(nodes) == 1 and isinstance(nodes[0], ast.If) and (
            nodes[0].body and self.parse_header(nodes[0].body[0])) and (
                not nodes[0].orelse or self.is_renpy_if(nodes[0].orelse) or
                self.parse_header(nodes[0].orelse[0]))

    def is_renpy_for(self, nodes):
        return (len(nodes) == 2 and isinstance(nodes[0], ast.Assign) and
            len(nodes[0].targets) == 1 and
            isinstance(nodes[0].targets[0], ast.Name) and
            re.match(r"_[0-9]+$", nodes[0].targets[0].id) and
            isinstance(nodes[0].value, ast.Num) and nodes[0].value.n == 0 and
            isinstance(nodes[1], ast.For) and not nodes[1].orelse and
            nodes[1].body and self.parse_header(nodes[1].body[0]) and
            isinstance(nodes[1].body[-1], ast.AugAssign) and
            isinstance(nodes[1].body[-1].op, ast.Add) and
            isinstance(nodes[1].body[-1].target, ast.Name) and
            re.match(r"_[0-9]+$", nodes[1].body[-1].target.id) and
            isinstance(nodes[1].body[-1].value, ast.Num) and
            nodes[1].body[-1].value.n == 1)

    def strip_parens(self, text):
        if text and text[0] == '(' and text[-1] == ')':
            return text[1:-1]
        else:
            return text

    def print_if(self, header, code):
        # Here we handle the if statement. It might be valid python but we can check for this by
        # checking for the header that should normally occur within the if statement.
        # The if statement parser might also generate a second header if there's more than one screen
        # statement enclosed in the if/elif/else statements. We'll take care of that too.
        self.advance_to_line(self.get_first_line(code))
        self.indent()
        self.write("if %s:" % self.strip_parens(self.to_source(code[0].test)))
        if (len(code[0].body) >= 2 and self.parse_header(code[0].body[0]) and
            self.parse_header(code[0].body[1])):
            body = code[0].body[1:]
        else:
            body = code[0].body
        with self.not_root():
            self.print_nodes(body, 1)
            if code[0].orelse:
                if self.is_renpy_if(code[0].orelse):
                    self.advance_to_line(code[0].orelse[0].test.lineno)
                    self.indent()
                    self.write("el") # beginning of "elif"
                    self.skip_indent_until_write = True
                    self.print_if(header, code[0].orelse)
                else:
                    self.indent()
                    self.write("else:")
                    if (len(code[0].orelse) >= 2 and
                        self.parse_header(code[0].orelse[0]) and
                        self.parse_header(code[0].orelse[1])):
                        orelse = code[0].orelse[1:]
                    else:
                        orelse = code[0].orelse
                    self.print_nodes(orelse, 1)

    def print_for(self, header, code):
        # Here we handle the for statement. Note that the for statement generates some extra python code to
        # Keep track of it's header indices. The first one is ignored by the statement parser,
        # the second line is just ingored here.
        line = code[1]
        self.advance_to_line(self.get_first_line(code))
        self.indent()
        self.write("for %s in %s:" % (
            self.strip_parens(self.to_source(line.target)),
            self.to_source(line.iter)))
        if (len(line.body) >= 3 and self.parse_header(line.body[0]) and
            self.parse_header(line.body[1])):
            body = line.body[1:]
        else:
            body = line.body
        with self.not_root():
            self.print_nodes(body[:-1], 1)

    @dispatch(('renpy', 'use_screen'))
    def print_use(self, header, code):
        # This function handles the use statement, which translates into a python expression "renpy.use_screen".
        # It would technically be possible for this to be a python statement, but the odds of this are very small.
        # renpy itself will insert some kwargs, we'll delete those and then parse the command here.
        if (len(code) != 1 or not code[0].value.args or
            not isinstance(code[0].value.args[0], ast.Str)):
            return self.print_python(header, code)
        args, kwargs, exargs, exkwargs = self.parse_args(code[0])
        kwargs = [(key, value) for key, value in kwargs if not
                  (key == '_scope' or key == '_name')]

        self.advance_to_line(self.get_first_line(code))
        self.indent()
        self.write("use %s" % code[0].value.args[0].s)
        args.pop(0)

        arglist = []
        if args or kwargs or exargs or exkwargs:
            self.write("(")
            arglist.extend(args)
            arglist.extend("%s=%s" % i for i in kwargs)
            if exargs:
                arglist.append("*%s" % exargs)
            if exkwargs:
                arglist.append("**%s" % exkwargs)
            self.write(", ".join(arglist))
            self.write(")")

    @dispatch(('_scope', 'setdefault'))
    def print_default(self, header, code):
        if (len(code) != 1 or code[0].value.keywords or code[0].value.kwargs or
            len(code[0].value.args) != 2 or code[0].value.starargs or
            not isinstance(code[0].value.args[0], ast.Str)):
            return self.print_python(header, code)
        self.advance_to_line(self.get_first_line(code))
        self.indent()
        self.write("default %s = %s" %
            (code[0].value.args[0].s, self.to_source(code[0].value.args[1])))

    # These never have a ui.close() at the end
    @dispatch(('ui', 'add'))
    @dispatch(('ui', 'imagebutton'))
    @dispatch(('ui', 'input'))
    @dispatch(('ui', 'key'))
    @dispatch(('ui', 'label'))
    @dispatch(('ui', 'text'))
    @dispatch(('ui', 'null'))
    @dispatch(('ui', 'mousearea'))
    @dispatch(('ui', 'textbutton'))
    @dispatch(('ui', 'timer'))
    @dispatch(('ui', 'bar'))
    @dispatch(('ui', 'vbar'))
    @dispatch(('ui', 'hotbar'))
    @dispatch(('ui', 'on'))
    @dispatch(('ui', 'image'))
    def print_nochild(self, header, code):
        if len(code) != 1:
            self.print_python(header, code)
            return
        line = code[0]
        self.advance_to_line(self.get_first_line(code))
        self.indent()
        self.write(line.value.func.attr)
        self.print_args(line.value)
        with self.not_root():
            self.print_buggy_keywords_and_nodes(
                self.make_printable_keywords(line.value.keywords,
                                             line.value.lineno),
                None, False, False)

    # These functions themselves don't have a ui.close() at the end, but
    # they're always immediately followed by one that does (usually
    # ui.child_or_fixed(), but also possibly one set with "has")
    @dispatch(('ui', 'button'))
    @dispatch(('ui', 'frame'))
    @dispatch(('ui', 'transform'))
    @dispatch(('ui', 'viewport'))
    @dispatch(('ui', 'window'))
    @dispatch(('ui', 'drag'))
    @dispatch(('ui', 'hotspot_with_child'))
    def print_onechild(self, header, code, has_block=False):
        # We expect to have at least ourself, one child, and ui.close()
        if len(code) < 3 or self.get_dispatch_key(code[-1]) != ('ui', 'close'):
            if has_block:
                raise BadHasBlockException()
            self.print_python(header, code)
            return
        line = code[0]
        name = line.value.func.attr
        if name == 'hotspot_with_child':
            name = 'hotspot'
        if self.get_dispatch_key(code[1]) != ('ui', 'child_or_fixed'):
            # Handle the case where a "has" statement was used
            if has_block:
                # Ren'Py lets users nest "has" blocks for some reason, and it
                # puts the ui.close() statement in the wrong place when they do.
                # Since we checked for ui.close() being in the right place
                # before, the only way we could ever get here is if a user added
                # one inside a python block at the end. If this happens, turn
                # the whole outer block into Python instead of screencode.
                raise BadHasBlockException()
            if not self.parse_header(code[1]):
                self.print_python(header, code)
                return
            block = code[1:]
            state = self.save_state()
            try:
                self.advance_to_line(self.get_first_line(code))
                self.indent()
                self.write(name)
                self.print_args(line.value)
                with self.not_root():
                    self.print_buggy_keywords_and_nodes(
                        self.make_printable_keywords(line.value.keywords,
                                                     line.value.lineno),
                        None, True, False)
                    with self.increase_indent():
                        if len(block) > 1 and isinstance(block[1], ast.Expr):
                            # If this isn't true, we'll get a BadHasBlockException
                            # later anyway. This check is just to keep it from being
                            # an exception that we can't handle.
                            self.advance_to_line(block[1].value.lineno)
                        self.indent()
                        self.write("has ")
                    self.skip_indent_until_write = True
                    self.print_nodes(block, 1, True)
            except BadHasBlockException as e:
                self.rollback_state(state)
                self.print_python(header, code)
            else:
                self.commit_state(state)
        else:
            # Remove ourself, ui.child_or_fixed(), and ui.close()
            block = code[2:-1]
            if block and not self.parse_header(block[0]):
                if has_block:
                    raise BadHasBlockException()
                self.print_python(header, code)
                return
            if not has_block:
                self.advance_to_line(self.get_first_line(code))
            self.indent()
            self.write(name)
            self.print_args(line.value)
            with self.not_root():
                self.print_buggy_keywords_and_nodes(
                    self.make_printable_keywords(line.value.keywords,
                                                 line.value.lineno),
                    block, False, has_block)

    # These always have a ui.close() at the end
    @dispatch(('ui', 'fixed'))
    @dispatch(('ui', 'grid'))
    @dispatch(('ui', 'hbox'))
    @dispatch(('ui', 'side'))
    @dispatch(('ui', 'vbox'))
    @dispatch(('ui', 'imagemap'))
    @dispatch(('ui', 'draggroup'))
    def print_manychildren(self, header, code, has_block=False):
        if (self.get_dispatch_key(code[-1]) != ('ui', 'close') or
            (len(code) != 2 and not self.parse_header(code[1]))):
            if has_block:
                raise BadHasBlockException()
            self.print_python(header, code)
            return
        line = code[0]
        block = code[1:-1]
        if not has_block:
            self.advance_to_line(self.get_first_line(code))
        self.indent()
        self.write(line.value.func.attr)
        self.print_args(line.value)
        with self.not_root():
            self.print_buggy_keywords_and_nodes(
                self.make_printable_keywords(line.value.keywords,
                                             line.value.lineno),
                block, False, has_block)

    # Parsing functions

    def parse_header(self, header):
        # Given a Python AST node, returns the parent ID if the node represents
        # a header, or None otherwise.
        if (isinstance(header, ast.Assign) and len(header.targets) == 1 and
                isinstance(header.targets[0], ast.Name) and
                re.match(r"_[0-9]+$", header.targets[0].id) and
                isinstance(header.value, ast.Tuple) and
                len(header.value.elts) == 2 and
                isinstance(header.value.elts[0], ast.Name)):
            parent_id = header.value.elts[0].id
            index = header.value.elts[1]
            if re.match(r"_([0-9]+|name)$", parent_id) and (
                    isinstance(index, ast.Num) or
                    (isinstance(index, ast.Name) and
                    re.match(r"_[0-9]+$", index.id))):
                return parent_id
        return None

    def parse_args(self, node):
        return ([self.to_source(i) for i in node.value.args],
            [(i.arg, self.to_source(i.value)) for i in node.value.keywords],
            node.value.starargs and self.to_source(node.value.starargs),
            node.value.kwargs and self.to_source(node.value.kwargs))

class BadHasBlockException(Exception):
    pass