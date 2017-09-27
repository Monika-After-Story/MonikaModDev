# Copyright (c) 2012 Yuri K. Schlesner
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
from util import DecompilerBase, First, WordConcatenator, reconstruct_paraminfo, \
                 reconstruct_arginfo, string_escape, split_logical_lines, Dispatcher
from util import say_get_code

from operator import itemgetter
from StringIO import StringIO

import magic
magic.fake_package(b"renpy")
import renpy

import screendecompiler
import sl2decompiler
import testcasedecompiler
import codegen
import astdump

__all__ = ["astdump", "codegen", "magic", "screendecompiler", "sl2decompiler", "testcasedecompiler", "translate", "util", "pprint", "Decompiler"]

# Main API

def pprint(out_file, ast, indent_level=0,
           decompile_python=False, printlock=None, translator=None, init_offset=False):
    Decompiler(out_file, printlock=printlock,
               decompile_python=decompile_python, translator=translator).dump(ast, indent_level, init_offset)

# Implementation

class Decompiler(DecompilerBase):
    """
    An object which hanldes the decompilation of renpy asts to a given stream
    """

    # This dictionary is a mapping of Class: unbount_method, which is used to determine
    # what method to call for which ast class
    dispatch = Dispatcher()

    def __init__(self, out_file=None, decompile_python=False,
                 indentation = '    ', printlock=None, translator=None):
        super(Decompiler, self).__init__(out_file, indentation, printlock)
        self.decompile_python = decompile_python
        self.translator = translator

        self.paired_with = False
        self.say_inside_menu = None
        self.label_inside_menu = None
        self.in_init = False
        self.missing_init = False
        self.init_offset = 0
        self.is_356c6e34_or_later = False

    def dump(self, ast, indent_level=0, init_offset=False):
        if (isinstance(ast, (tuple, list)) and len(ast) > 1 and
            isinstance(ast[-1], renpy.ast.Return) and
            (not hasattr(ast[-1], 'expression') or ast[-1].expression is None) and
            ast[-1].linenumber == ast[-2].linenumber):
            # A very crude version check, but currently the best we can do.
            # Note that this commit first appears in the 6.99 release.
            self.is_356c6e34_or_later = True

        if self.translator:
            self.translator.translate_dialogue(ast)

        if init_offset and isinstance(ast, (tuple, list)):
            self.set_best_init_offset(ast)

        # skip_indent_until_write avoids an initial blank line
        super(Decompiler, self).dump(ast, indent_level, skip_indent_until_write=True)
        # if there's anything we wanted to write out but didn't yet, do it now
        for m in self.blank_line_queue:
            m(None)
        self.write("\n# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc\n")
        assert not self.missing_init, "A required init, init label, or translate block was missing"

    def print_node(self, ast):
        # We special-case line advancement for TranslateString in its print
        # method, so don't advance lines for it here.
        if hasattr(ast, 'linenumber') and not isinstance(ast, renpy.ast.TranslateString):
            self.advance_to_line(ast.linenumber)
        # It doesn't matter what line "block:" is on. The loc of a RawBlock
        # refers to the first statement inside the block, which we advance
        # to from print_atl.
        elif hasattr(ast, 'loc') and not isinstance(ast, renpy.atl.RawBlock):
            self.advance_to_line(ast.loc[1])
        self.dispatch.get(type(ast), type(self).print_unknown)(self, ast)

    # ATL printing functions

    def print_atl(self, ast):
        with self.increase_indent():
            self.advance_to_line(ast.loc[1])
            if ast.statements:
                self.print_nodes(ast.statements)
            # If a statement ends with a colon but has no block after it, loc will
            # get set to ('', 0). That isn't supposed to be valid syntax, but it's
            # the only thing that can generate that.
            elif ast.loc != ('', 0):
                self.indent()
                self.write("pass")

    @dispatch(renpy.atl.RawMultipurpose)
    def print_atl_rawmulti(self, ast):
        warp_words = WordConcatenator(False)

        # warpers
        if ast.warp_function:
            warp_words.append("warp", ast.warp_function, ast.duration)
        elif ast.warper:
            warp_words.append(ast.warper, ast.duration)
        elif ast.duration != "0":
            warp_words.append("pause", ast.duration)

        warp = warp_words.join()
        words = WordConcatenator(warp and warp[-1] != ' ', True)

        # revolution
        if ast.revolution:
            words.append(ast.revolution)

        # circles
        if ast.circles != "0":
            words.append("circles %s" % ast.circles)

        # splines
        spline_words = WordConcatenator(False)
        for name, expressions in ast.splines:
            spline_words.append(name)
            for expression in expressions:
                spline_words.append("knot", expression)
        words.append(spline_words.join())

        # properties
        property_words = WordConcatenator(False)
        for key, value in ast.properties:
            property_words.append(key, value)
        words.append(property_words.join())

        # with
        expression_words = WordConcatenator(False)
        # TODO There's a lot of cases where pass isn't needed, since we could
        # reorder stuff so there's never 2 expressions in a row. (And it's never
        # necessary for the last one, but we don't know what the last one is
        # since it could get reordered.)
        needs_pass = len(ast.expressions) > 1
        for (expression, with_expression) in ast.expressions:
            expression_words.append(expression)
            if with_expression:
                expression_words.append("with", with_expression)
            if needs_pass:
                expression_words.append("pass")
        words.append(expression_words.join())

        to_write = warp + words.join()
        if to_write:
            self.indent()
            self.write(to_write)
        else:
            # A trailing comma results in an empty RawMultipurpose being
            # generated on the same line as the last real one.
            self.write(",")

    @dispatch(renpy.atl.RawBlock)
    def print_atl_rawblock(self, ast):
        self.indent()
        self.write("block:")
        self.print_atl(ast)

    @dispatch(renpy.atl.RawChild)
    def print_atl_rawchild(self, ast):
        for child in ast.children:
            self.indent()
            self.write("contains:")
            self.print_atl(child)

    @dispatch(renpy.atl.RawChoice)
    def print_atl_rawchoice(self, ast):
        for chance, block in ast.choices:
            self.indent()
            self.write("choice")
            if chance != "1.0":
                self.write(" %s" % chance)
            self.write(":")
            self.print_atl(block)
        if (self.index + 1 < len(self.block) and
            isinstance(self.block[self.index + 1], renpy.atl.RawChoice)):
            self.indent()
            self.write("pass")

    @dispatch(renpy.atl.RawContainsExpr)
    def print_atl_rawcontainsexpr(self, ast):
        self.indent()
        self.write("contains %s" % ast.expression)

    @dispatch(renpy.atl.RawEvent)
    def print_atl_rawevent(self, ast):
        self.indent()
        self.write("event %s" % ast.name)

    @dispatch(renpy.atl.RawFunction)
    def print_atl_rawfunction(self, ast):
        self.indent()
        self.write("function %s" % ast.expr)

    @dispatch(renpy.atl.RawOn)
    def print_atl_rawon(self, ast):
        for name, block in sorted(ast.handlers.items(),
                                  key=lambda i: i[1].loc[1]):
            self.indent()
            self.write("on %s:" % name)
            self.print_atl(block)

    @dispatch(renpy.atl.RawParallel)
    def print_atl_rawparallel(self, ast):
        for block in ast.blocks:
            self.indent()
            self.write("parallel:")
            self.print_atl(block)
        if (self.index + 1 < len(self.block) and
            isinstance(self.block[self.index + 1], renpy.atl.RawParallel)):
            self.indent()
            self.write("pass")

    @dispatch(renpy.atl.RawRepeat)
    def print_atl_rawrepeat(self, ast):
        self.indent()
        self.write("repeat")
        if ast.repeats:
            self.write(" %s" % ast.repeats) # not sure if this is even a string

    @dispatch(renpy.atl.RawTime)
    def print_atl_rawtime(self, ast):
        self.indent()
        self.write("time %s" % ast.time)

    # Displayable related functions

    def print_imspec(self, imspec):
        if imspec[1] is not None:
            begin = "expression %s" % imspec[1]
        else:
            begin = " ".join(imspec[0])

        words = WordConcatenator(begin and begin[-1] != ' ', True)
        if imspec[2] is not None:
            words.append("as %s" % imspec[2])

        if len(imspec[6]) > 0:
            words.append("behind %s" % ', '.join(imspec[6]))

        if isinstance(imspec[4], unicode):
            words.append("onlayer %s" % imspec[4])

        if imspec[5] is not None:
            words.append("zorder %s" % imspec[5])

        if len(imspec[3]) > 0:
            words.append("at %s" % ', '.join(imspec[3]))

        self.write(begin + words.join())
        return words.needs_space

    @dispatch(renpy.ast.Image)
    def print_image(self, ast):
        self.require_init()
        self.indent()
        self.write("image %s" % ' '.join(ast.imgname))
        if ast.code is not None:
            self.write(" = %s" % ast.code.source)
        else:
            if hasattr(ast, "atl") and ast.atl is not None:
                self.write(":")
                self.print_atl(ast.atl)

    @dispatch(renpy.ast.Transform)
    def print_transform(self, ast):
        self.require_init()
        self.indent()

        # If we have an implicit init block with a non-default priority, we need to store the priority here.
        priority = ""
        if isinstance(self.parent, renpy.ast.Init):
            init = self.parent
            if init.priority != self.init_offset and len(init.block) == 1 and not self.should_come_before(init, ast):
                priority = " %d" % (init.priority - self.init_offset)
        self.write("transform%s %s" % (priority, ast.varname))
        if ast.parameters is not None:
            self.write(reconstruct_paraminfo(ast.parameters))

        if hasattr(ast, "atl") and ast.atl is not None:
            self.write(":")
            self.print_atl(ast.atl)

    # Directing related functions

    @dispatch(renpy.ast.Show)
    def print_show(self, ast):
        self.indent()
        self.write("show ")
        needs_space = self.print_imspec(ast.imspec)

        if self.paired_with:
            if needs_space:
                self.write(" ")
            self.write("with %s" % self.paired_with)
            self.paired_with = True

        if hasattr(ast, "atl") and ast.atl is not None:
            self.write(":")
            self.print_atl(ast.atl)

    @dispatch(renpy.ast.ShowLayer)
    def print_showlayer(self, ast):
        self.indent()
        self.write("show layer %s" % ast.layer)

        if ast.at_list:
            self.write(" at %s" % ', '.join(ast.at_list))

        if hasattr(ast, "atl") and ast.atl is not None:
            self.write(":")
            self.print_atl(ast.atl)

    @dispatch(renpy.ast.Scene)
    def print_scene(self, ast):
        self.indent()
        self.write("scene")

        if ast.imspec is None:
            if isinstance(ast.layer, unicode):
                self.write(" onlayer %s" % ast.layer)
            needs_space = True
        else:
            self.write(" ")
            needs_space = self.print_imspec(ast.imspec)

        if self.paired_with:
            if needs_space:
                self.write(" ")
            self.write("with %s" % self.paired_with)
            self.paired_with = True

        if hasattr(ast, "atl") and ast.atl is not None:
            self.write(":")
            self.print_atl(ast.atl)

    @dispatch(renpy.ast.Hide)
    def print_hide(self, ast):
        self.indent()
        self.write("hide ")
        needs_space = self.print_imspec(ast.imspec)
        if self.paired_with:
            if needs_space:
                self.write(" ")
            self.write("with %s" % self.paired_with)
            self.paired_with = True

    @dispatch(renpy.ast.With)
    def print_with(self, ast):
        # the 'paired' attribute indicates that this with
        # and with node afterwards are part of a postfix
        # with statement. detect this and process it properly
        if hasattr(ast, "paired") and ast.paired is not None:
            # Sanity check. check if there's a matching with statement two nodes further
            if not(isinstance(self.block[self.index + 2], renpy.ast.With) and
                   self.block[self.index + 2].expr == ast.paired):
                raise Exception("Unmatched paired with {0} != {1}".format(
                                repr(self.paired_with), repr(ast.expr)))

            self.paired_with = ast.paired

        elif self.paired_with:
            # Check if it was consumed by a show/scene statement
            if self.paired_with is not True:
                self.write(" with %s" % ast.expr)
            self.paired_with = False
        else:
            self.indent()
            self.write("with %s" % ast.expr)
            self.paired_with = False

    # Flow control

    @dispatch(renpy.ast.Label)
    def print_label(self, ast):
        # If a Call block preceded us, it printed us as "from"
        if (self.index and isinstance(self.block[self.index - 1], renpy.ast.Call)):
            return
        remaining_blocks = len(self.block) - self.index
        # See if we're the label for a menu, rather than a standalone label.
        if remaining_blocks > 1 and not ast.block and (not hasattr(ast, 'parameters') or ast.parameters is None):
            next_ast = self.block[self.index + 1]
            if (hasattr(next_ast, 'linenumber') and next_ast.linenumber == ast.linenumber and
                (isinstance(next_ast, renpy.ast.Menu) or (remaining_blocks > 2 and
                isinstance(next_ast, renpy.ast.Say) and
                self.say_belongs_to_menu(next_ast, self.block[self.index + 2])))):
                self.label_inside_menu = ast
                return
        self.indent()

        # It's possible that we're an "init label", not a regular label. There's no way to know
        # if we are until we parse our children, so temporarily redirect all of our output until
        # that's done, so that we can squeeze in an "init " if we are.
        out_file = self.out_file
        self.out_file = StringIO()
        missing_init = self.missing_init
        self.missing_init = False
        try:
            self.write("label %s%s%s:" % (
                ast.name,
                reconstruct_paraminfo(ast.parameters) if hasattr(ast, 'parameters') else '',
                " hide" if hasattr(ast, 'hide') and ast.hide else ""))
            self.print_nodes(ast.block, 1)
        finally:
            if self.missing_init:
                out_file.write("init ")
            self.missing_init = missing_init
            out_file.write(self.out_file.getvalue())
            self.out_file = out_file

    @dispatch(renpy.ast.Jump)
    def print_jump(self, ast):
        self.indent()
        self.write("jump %s%s" % ("expression " if ast.expression else "", ast.target))

    @dispatch(renpy.ast.Call)
    def print_call(self, ast):
        self.indent()
        words = WordConcatenator(False)
        words.append("call")
        if ast.expression:
            words.append("expression")
        words.append(ast.label)

        if hasattr(ast, 'arguments') and ast.arguments is not None:
            if ast.expression:
                words.append("pass")
            words.append(reconstruct_arginfo(ast.arguments))

        # We don't have to check if there's enough elements here,
        # since a Label or a Pass is always emitted after a Call.
        next_block = self.block[self.index + 1]
        if isinstance(next_block, renpy.ast.Label):
            words.append("from %s" % next_block.name)

        self.write(words.join())

    @dispatch(renpy.ast.Return)
    def print_return(self, ast):
        if ((not hasattr(ast, 'expression') or ast.expression is None) and self.parent is None and
            self.index + 1 == len(self.block) and self.index and
            ast.linenumber == self.block[self.index - 1].linenumber):
            # As of Ren'Py commit 356c6e34, a return statement is added to
            # the end of each rpyc file. Don't include this in the source.
            return

        self.indent()
        self.write("return")

        if hasattr(ast, 'expression') and ast.expression is not None:
            self.write(" %s" % ast.expression)

    @dispatch(renpy.ast.If)
    def print_if(self, ast):
        statement = First("if %s:", "elif %s:")

        for i, (condition, block) in enumerate(ast.entries):
            # The non-Unicode string "True" is the condition for else:.
            if (i + 1) == len(ast.entries) and not isinstance(condition, unicode):
                self.indent()
                self.write("else:")
            else:
                if(hasattr(condition, 'linenumber')):
                    self.advance_to_line(condition.linenumber)
                self.indent()
                self.write(statement() % condition)

            self.print_nodes(block, 1)

    @dispatch(renpy.ast.While)
    def print_while(self, ast):
        self.indent()
        self.write("while %s:" % ast.condition)

        self.print_nodes(ast.block, 1)

    @dispatch(renpy.ast.Pass)
    def print_pass(self, ast):
        if (self.index and
            isinstance(self.block[self.index - 1], renpy.ast.Call)):
            return

        if (self.index > 1 and
            isinstance(self.block[self.index - 2], renpy.ast.Call) and
            isinstance(self.block[self.index - 1], renpy.ast.Label) and
            self.block[self.index - 2].linenumber == ast.linenumber):
            return

        self.indent()
        self.write("pass")

    def should_come_before(self, first, second):
        return first.linenumber < second.linenumber

    def require_init(self):
        if not self.in_init:
            self.missing_init = True

    def set_best_init_offset(self, nodes):
        votes = {}
        for ast in nodes:
            if not isinstance(ast, renpy.ast.Init):
                continue
            offset = ast.priority
            # Keep this block in sync with print_init
            if len(ast.block) == 1 and not self.should_come_before(ast, ast.block[0]):
                if isinstance(ast.block[0], renpy.ast.Screen):
                    offset -= -500
                elif isinstance(ast.block[0], renpy.ast.Testcase):
                    offset -= 500
                elif isinstance(ast.block[0], renpy.ast.Image):
                    offset -= 500 if self.is_356c6e34_or_later else 990
            votes[offset] = votes.get(offset, 0) + 1
        if votes:
            winner = max(votes, key=votes.get)
            # It's only worth setting an init offset if it would save
            # more than one priority specification versus not setting one.
            if votes.get(0, 0) + 1 < votes[winner]:
                self.set_init_offset(winner)

    def set_init_offset(self, offset):
        def do_set_init_offset(linenumber):
            # if we got to the end of the file and haven't emitted this yet,
            # don't bother, since it only applies to stuff below it.
            if linenumber is None or linenumber - self.linenumber <= 1 or self.indent_level:
                return True
            if offset != self.init_offset:
                self.indent()
                self.write("init offset = %s" % offset)
                self.init_offset = offset
            return False

        self.do_when_blank_line(do_set_init_offset)

    @dispatch(renpy.ast.Init)
    def print_init(self, ast):
        in_init = self.in_init
        self.in_init = True
        try:
            # A bunch of statements can have implicit init blocks
            # Define has a default priority of 0, screen of -500 and image of 990
            # Keep this block in sync with set_best_init_offset
            # TODO merge this and require_init into another decorator or something
            if len(ast.block) == 1 and (
                isinstance(ast.block[0], (renpy.ast.Define,
                                          renpy.ast.Default,
                                          renpy.ast.Transform)) or
                (ast.priority == -500 + self.init_offset and isinstance(ast.block[0], renpy.ast.Screen)) or
                (ast.priority == self.init_offset and isinstance(ast.block[0], renpy.ast.Style)) or
                (ast.priority == 500 + self.init_offset and isinstance(ast.block[0], renpy.ast.Testcase)) or
                # Images had their default init priority changed in commit 679f9e31 (Ren'Py 6.99.10).
                # We don't have any way of detecting this commit, though. The closest one we can
                # detect is 356c6e34 (Ren'Py 6.99). For any versions in between these, we'll emit
                # an unnecessary "init 990 " before image statements, but this doesn't affect the AST,
                # and any other solution would result in incorrect code being generated in some cases.
                (ast.priority == (500 if self.is_356c6e34_or_later else 990) + self.init_offset and isinstance(ast.block[0], renpy.ast.Image))) and not (
                self.should_come_before(ast, ast.block[0])):
                # If they fulfill this criteria we just print the contained statement
                self.print_nodes(ast.block)

            # translatestring statements are split apart and put in an init block.
            elif (len(ast.block) > 0 and
                    ast.priority == self.init_offset and
                    all(isinstance(i, renpy.ast.TranslateString) for i in ast.block) and
                    all(i.language == ast.block[0].language for i in ast.block[1:])):
                self.print_nodes(ast.block)

            else:
                self.indent()
                self.write("init")
                if ast.priority != self.init_offset:
                    self.write(" %d" % (ast.priority - self.init_offset))

                if len(ast.block) == 1 and not self.should_come_before(ast, ast.block[0]):
                    self.write(" ")
                    self.skip_indent_until_write = True
                    self.print_nodes(ast.block)
                else:
                    self.write(":")
                    self.print_nodes(ast.block, 1)
        finally:
            self.in_init = in_init

    @dispatch(renpy.ast.Menu)
    def print_menu(self, ast):
        self.indent()
        self.write("menu")
        if self.label_inside_menu is not None:
            self.write(" %s" % self.label_inside_menu.name)
            self.label_inside_menu = None
        self.write(":")
        with self.increase_indent():
            if self.say_inside_menu is not None:
                self.print_say(self.say_inside_menu, inmenu=True)
                self.say_inside_menu = None

            if ast.with_ is not None:
                self.indent()
                self.write("with %s" % ast.with_)

            if ast.set is not None:
                self.indent()
                self.write("set %s" % ast.set)

            for label, condition, block in ast.items:
                if self.translator:
                    label = self.translator.strings.get(label, label)

                if isinstance(condition, unicode):
                    self.advance_to_line(condition.linenumber)
                self.indent()
                self.write('"%s"' % string_escape(label))

                if block is not None:
                    if isinstance(condition, unicode):
                        self.write(" if %s" % condition)
                    self.write(":")
                    self.print_nodes(block, 1)

    # Programming related functions

    @dispatch(renpy.ast.Python)
    def print_python(self, ast, early=False):
        self.indent()

        code = ast.code.source
        if code[0] == '\n':
            code = code[1:]
            self.write("python")
            if early:
                self.write(" early")
            if ast.hide:
                self.write(" hide")
            if hasattr(ast, "store") and ast.store != "store":
                self.write(" in ")
                # Strip prepended "store."
                self.write(ast.store[6:])
            self.write(":")

            with self.increase_indent():
                self.write_lines(split_logical_lines(code))

        else:
            self.write("$ %s" % code)

    @dispatch(renpy.ast.EarlyPython)
    def print_earlypython(self, ast):
        self.print_python(ast, early=True)

    @dispatch(renpy.ast.Define)
    @dispatch(renpy.ast.Default)
    def print_define(self, ast):
        self.require_init()
        self.indent()
        if isinstance(ast, renpy.ast.Default):
            name = "default"
        else:
            name = "define"

        # If we have an implicit init block with a non-default priority, we need to store the priority here.
        priority = ""
        if isinstance(self.parent, renpy.ast.Init):
            init = self.parent
            if init.priority != self.init_offset and len(init.block) == 1 and not self.should_come_before(init, ast):
                priority = " %d" % (init.priority - self.init_offset)
        if not hasattr(ast, "store") or ast.store == "store":
            self.write("%s%s %s = %s" % (name, priority, ast.varname, ast.code.source))
        else:
            self.write("%s%s %s.%s = %s" % (name, priority, ast.store[6:], ast.varname, ast.code.source))

    # Specials

    # Returns whether a Say statement immediately preceding a Menu statement
    # actually belongs inside of the Menu statement.
    def say_belongs_to_menu(self, say, menu):
        return (not say.interact and say.who is not None and
            say.with_ is None and 
            (not hasattr(say, "attributes") or say.attributes is None) and
            isinstance(menu, renpy.ast.Menu) and
            menu.items[0][2] is not None and
            not self.should_come_before(say, menu))

    @dispatch(renpy.ast.Say)
    def print_say(self, ast, inmenu=False):
        if (not inmenu and self.index + 1 < len(self.block) and
            self.say_belongs_to_menu(ast, self.block[self.index + 1])):
            self.say_inside_menu = ast
            return
        self.indent()
        self.write(say_get_code(ast, inmenu))

    @dispatch(renpy.ast.UserStatement)
    def print_userstatement(self, ast):
        self.indent()
        self.write(ast.line)

    @dispatch(renpy.ast.Style)
    def print_style(self, ast):
        self.require_init()
        keywords = {ast.linenumber: WordConcatenator(False, True)}

        # These don't store a line number, so just put them on the first line
        if ast.parent is not None:
            keywords[ast.linenumber].append("is %s" % ast.parent)
        if ast.clear:
            keywords[ast.linenumber].append("clear")
        if ast.take is not None:
            keywords[ast.linenumber].append("take %s" % ast.take)
        for delname in ast.delattr:
            keywords[ast.linenumber].append("del %s" % delname)

        # These do store a line number
        if ast.variant is not None:
            if ast.variant.linenumber not in keywords:
                keywords[ast.variant.linenumber] = WordConcatenator(False)
            keywords[ast.variant.linenumber].append("variant %s" % ast.variant)
        for key, value in ast.properties.iteritems():
            if value.linenumber not in keywords:
                keywords[value.linenumber] = WordConcatenator(False)
            keywords[value.linenumber].append("%s %s" % (key, value))

        keywords = sorted([(k, v.join()) for k, v in keywords.items()],
                          key=itemgetter(0))
        self.indent()
        self.write("style %s" % ast.style_name)
        if keywords[0][1]:
            self.write(" %s" % keywords[0][1])
        if len(keywords) > 1:
            self.write(":")
            with self.increase_indent():
                for i in keywords[1:]:
                    self.advance_to_line(i[0])
                    self.indent()
                    self.write(i[1])

    # Translation functions

    @dispatch(renpy.ast.Translate)
    def print_translate(self, ast):
        self.indent()
        self.write("translate %s %s:" % (ast.language or "None", ast.identifier))

        self.print_nodes(ast.block, 1)

    @dispatch(renpy.ast.EndTranslate)
    def print_endtranslate(self, ast):
        # an implicitly added node which does nothing...
        pass

    @dispatch(renpy.ast.TranslateString)
    def print_translatestring(self, ast):
        self.require_init()
        # Was the last node a translatestrings node?
        if not(self.index and
               isinstance(self.block[self.index - 1], renpy.ast.TranslateString) and
               self.block[self.index - 1].language == ast.language):
            self.indent()
            self.write("translate %s strings:" % ast.language or "None")

        # TranslateString's linenumber refers to the line with "old", not to the
        # line with "translate %s strings:"
        with self.increase_indent():
            self.advance_to_line(ast.linenumber)
            self.indent()
            self.write('old "%s"' % string_escape(ast.old))
            self.indent()
            self.write('new "%s"' % string_escape(ast.new))

    @dispatch(renpy.ast.TranslateBlock)
    def print_translateblock(self, ast):
        self.indent()
        self.write("translate %s " % (ast.language or "None"))

        self.skip_indent_until_write = True

        in_init = self.in_init
        if len(ast.block) == 1 and isinstance(ast.block[0], (renpy.ast.Python, renpy.ast.Style)):
            # Ren'Py counts the TranslateBlock from "translate python" and "translate style" as an Init.
            self.in_init = True
        try:
            self.print_nodes(ast.block)
        finally:
            self.in_init = in_init

    # Screens

    @dispatch(renpy.ast.Screen)
    def print_screen(self, ast):
        self.require_init()
        screen = ast.screen
        if isinstance(screen, renpy.screenlang.ScreenLangScreen):
            self.linenumber = screendecompiler.pprint(self.out_file, screen, self.indent_level,
                                    self.linenumber,
                                    self.decompile_python,
                                    self.skip_indent_until_write,
                                    self.printlock)
            self.skip_indent_until_write = False

        elif isinstance(screen, renpy.sl2.slast.SLScreen):
            self.linenumber = sl2decompiler.pprint(self.out_file, screen, self.indent_level,
                                    self.linenumber,
                                    self.skip_indent_until_write,
                                    self.printlock)
            self.skip_indent_until_write = False
        else:
            self.print_unknown(screen)

    # Testcases

    @dispatch(renpy.ast.Testcase)
    def print_testcase(self, ast):
        self.require_init()
        self.indent()
        self.write('testcase %s:' % ast.label)
        self.linenumber = testcasedecompiler.pprint(self.out_file, ast.test.block, self.indent_level + 1,
                                self.linenumber,
                                self.skip_indent_until_write,
                                self.printlock)
        self.skip_indent_until_write = False
