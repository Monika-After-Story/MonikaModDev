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
import sys
from operator import itemgetter

from util import DecompilerBase, First, reconstruct_paraminfo, \
                 reconstruct_arginfo, split_logical_lines, Dispatcher

from renpy import ui, sl2
from renpy.text import text
from renpy.sl2 import sldisplayables as sld
from renpy.display import layout, behavior, im, motion, dragdrop

# Main API

def pprint(out_file, ast, indent_level=0, linenumber=1,
           skip_indent_until_write=False, printlock=None):
    return SL2Decompiler(out_file, printlock=printlock).dump(
        ast, indent_level, linenumber, skip_indent_until_write)

# Implementation

class SL2Decompiler(DecompilerBase):
    """
    An object which handles the decompilation of renpy screen language 2 screens to a given stream
    """

    # This dictionary is a mapping of Class: unbound_method, which is used to determine
    # what method to call for which slast class
    dispatch = Dispatcher()

    def print_node(self, ast):
        self.advance_to_line(ast.location[1])
        self.dispatch.get(type(ast), type(self).print_unknown)(self, ast)

    @dispatch(sl2.slast.SLScreen)
    def print_screen(self, ast):

        # Print the screen statement and create the block
        self.indent()
        self.write("screen %s" % ast.name)
        # If we have parameters, print them.
        if ast.parameters:
            self.write(reconstruct_paraminfo(ast.parameters))
        # Print any keywords
        if ast.tag:
            self.write(" tag %s" % ast.tag)
        # If we're decompiling screencode, print it. Else, insert a pass statement
        self.print_keywords_and_children(ast.keyword,
            ast.children, ast.location[1])

    @dispatch(sl2.slast.SLIf)
    def print_if(self, ast):
        # if and showif share a lot of the same infrastructure
        self._print_if(ast, "if")

    @dispatch(sl2.slast.SLShowIf)
    def print_showif(self, ast):
        # so for if and showif we just call an underlying function with an extra argument
        self._print_if(ast, "showif")

    def _print_if(self, ast, keyword):
        # the first condition is named if or showif, the rest elif
        keyword = First(keyword, "elif")
        for condition, block in ast.entries:
            self.advance_to_line(block.location[1])
            self.indent()
            # if condition is None, this is the else clause
            if condition is None:
                self.write("else:")
            else:
                self.write("%s %s:" % (keyword(), condition))

            # Every condition has a block of type slast.SLBlock
            if block.keyword or block.children:
                self.print_block(block)
            else:
                with self.increase_indent():
                    self.indent()
                    self.write("pass")

    @dispatch(sl2.slast.SLBlock)
    def print_block(self, ast):
        # A block contains possible keyword arguments and a list of child nodes
        # this is the reason if doesn't keep a list of children but special Blocks
        self.print_keywords_and_children(ast.keyword, ast.children, None)

    @dispatch(sl2.slast.SLFor)
    def print_for(self, ast):
        # Since tuple unpickling is hard, renpy just gives up and inserts a
        # $ a,b,c = _sl2_i after the for statement if any tuple unpacking was
        # attempted in the for statement. Detect this and ignore this slast.SLPython entry
        if ast.variable == "_sl2_i":
            variable = ast.children[0].code.source[:-9]
            children = ast.children[1:]
        else:
            variable = ast.variable.strip() + " "
            children = ast.children

        self.indent()
        self.write("for %sin %s:" % (variable, ast.expression))

        # Interestingly, for doesn't contain a block, but just a list of child nodes
        self.print_nodes(children, 1)

    @dispatch(sl2.slast.SLPython)
    def print_python(self, ast):
        self.indent()

        # Extract the source code from the slast.SLPython object. If it starts with a
        # newline, print it as a python block, else, print it as a $ statement
        code = ast.code.source
        if code[0] == "\n":
            code = code[1:]
            self.write("python:")
            with self.increase_indent():
                self.write_lines(split_logical_lines(code))
        else:
            self.write("$ %s" % code)

    @dispatch(sl2.slast.SLPass)
    def print_pass(self, ast):
        # A pass statement
        self.indent()
        self.write("pass")

    @dispatch(sl2.slast.SLUse)
    def print_use(self, ast):
        # A use statement requires reconstructing the arguments it wants to pass
        self.indent()
        self.write("use %s%s" % (ast.target, reconstruct_arginfo(ast.args)))
        if hasattr(ast, 'id') and ast.id is not None:
            self.write(" id %s" % ast.id)

        if hasattr(ast, 'block') and ast.block:
            self.write(":")
            self.print_block(ast.block)

    @dispatch(sl2.slast.SLTransclude)
    def print_transclude(self, ast):
        self.indent()
        self.write("transclude")

    @dispatch(sl2.slast.SLDefault)
    def print_default(self, ast):
        # A default statement
        self.indent()
        self.write("default %s = %s" % (ast.variable, ast.expression))

    @dispatch(sl2.slast.SLDisplayable)
    def print_displayable(self, ast, has_block=False):
        # slast.SLDisplayable represents a variety of statements. We can figure out
        # what statement it represents by analyzing the called displayable and style
        # attributes.
        key = (ast.displayable, ast.style)
        nameAndChildren = self.displayable_names.get(key)
        if nameAndChildren is None:
            self.write_failure("Unknown SL2 displayable: %s" % str(key))
        else:
            (name, children) = nameAndChildren
            self.indent()
            self.write(name)
            if ast.positional:
                self.write(" " + " ".join(ast.positional))
            # The AST contains no indication of whether or not "has" blocks
            # were used. We'll use one any time it's possible (except for
            # directly nesting them, or if they wouldn't contain any children),
            # since it results in cleaner code.
            if (not has_block and children == 1 and len(ast.children) == 1 and
                isinstance(ast.children[0], sl2.slast.SLDisplayable) and
                ast.children[0].children and (not ast.keyword or
                    ast.children[0].location[1] > ast.keyword[-1][1].linenumber)):
                self.print_keywords_and_children(ast.keyword, [],
                    ast.location[1], needs_colon=True)
                self.advance_to_line(ast.children[0].location[1])
                with self.increase_indent():
                    self.indent()
                    self.write("has ")
                    self.skip_indent_until_write = True
                    self.print_displayable(ast.children[0], True)
            else:
                self.print_keywords_and_children(ast.keyword, ast.children,
                     ast.location[1], has_block=has_block)

    displayable_names = {
        (behavior.OnEvent, None):          ("on", 0),
        (behavior.OnEvent, 0):             ("on", 0),
        (behavior.MouseArea, 0):           ("mousearea", 0),
        (ui._add, None):                   ("add", 0),
        (sld.sl2add, None):                ("add", 0),
        (ui._hotbar, "hotbar"):            ("hotbar", 0),
        (sld.sl2vbar, None):               ("vbar", 0),
        (sld.sl2bar, None):                ("bar", 0),
        (ui._label, "label"):              ("label", 0),
        (ui._textbutton, 0):               ("textbutton", 0),
        (ui._imagebutton, "image_button"): ("imagebutton", 0),
        (im.image, "default"):             ("image", 0),
        (behavior.Input, "input"):         ("input", 0),
        (behavior.Timer, "default"):       ("timer", 0),
        (ui._key, None):                   ("key", 0),
        (text.Text, "text"):               ("text", 0),
        (layout.Null, "default"):          ("null", 0),
        (dragdrop.Drag, None):             ("drag", 1),
        (dragdrop.Drag, "drag"):           ("drag", 1),
        (motion.Transform, "transform"):   ("transform", 1),
        (ui._hotspot, "hotspot"):          ("hotspot", 1),
        (sld.sl2viewport, "viewport"):     ("viewport", 1),
        (behavior.Button, "button"):       ("button", 1),
        (layout.Window, "frame"):          ("frame", 1),
        (layout.Window, "window"):         ("window", 1),
        (dragdrop.DragGroup, None):        ("draggroup", 'many'),
        (ui._imagemap, "imagemap"):        ("imagemap", 'many'),
        (layout.Side, "side"):             ("side", 'many'),
        (layout.Grid, "grid"):             ("grid", 'many'),
        (sld.sl2vpgrid, "vpgrid"):         ("vpgrid", 'many'),
        (layout.MultiBox, "fixed"):        ("fixed", 'many'),
        (layout.MultiBox, "vbox"):         ("vbox", 'many'),
        (layout.MultiBox, "hbox"):         ("hbox", 'many')
    }

    def print_keywords_and_children(self, keywords, children, lineno, needs_colon=False, has_block=False):
        # This function prints the keyword arguments and child nodes
        # Used in a displayable screen statement

        # If lineno is None, we're already inside of a block.
        # Otherwise, we're on the line that could start a block.
        keywords_by_line = []
        current_line = (lineno, [])
        for key, value in keywords:
            if value is None:
                value = ""
                if current_line[0] is None:
                    keywords_by_line.append(current_line)
                    current_line = (0, [])
            elif current_line[0] is None or value.linenumber > current_line[0]:
                keywords_by_line.append(current_line)
                current_line = (value.linenumber, [])
            current_line[1].extend((key, value))
        keywords_by_line.append(current_line)
        last_keyword_line = keywords_by_line[-1][0]
        children_with_keywords = []
        children_after_keywords = []
        for i in children:
            if i.location[1] > last_keyword_line:
                children_after_keywords.append(i)
            else:
                children_with_keywords.append((i.location[1], i))
        # the keywords in keywords_by_line[0] go on the line that starts the
        # block, not in it
        block_contents = sorted(keywords_by_line[1:] + children_with_keywords,
                                key=itemgetter(0))
        if keywords_by_line[0][1]: # this never happens if lineno was None
            self.write(" %s" % ' '.join(keywords_by_line[0][1]))
        if block_contents or (not has_block and children_after_keywords):
            if lineno is not None:
                self.write(":")
            with self.increase_indent():
                for i in block_contents:
                    if isinstance(i[1], list):
                        self.advance_to_line(i[0])
                        self.indent()
                        self.write(' '.join(i[1]))
                    else:
                        self.print_node(i[1])
        elif needs_colon:
            self.write(":")
        self.print_nodes(children_after_keywords, 0 if has_block else 1)