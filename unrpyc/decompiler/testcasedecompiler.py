# Copyright (c) 2016 Jackmcbarn
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
from util import DecompilerBase, split_logical_lines, Dispatcher, string_escape
from renpy.test import testast

# Main API

def pprint(out_file, ast, indent_level=0, linenumber=1,
           skip_indent_until_write=False, printlock=None):
    return TestcaseDecompiler(out_file, printlock=printlock).dump(
        ast, indent_level, linenumber, skip_indent_until_write)

# Implementation

class TestcaseDecompiler(DecompilerBase):
    """
    An object which handles the decompilation of renpy testcase statements
    """

    # This dictionary is a mapping of Class: unbound_method, which is used to determine
    # what method to call for which testast class
    dispatch = Dispatcher()

    def print_node(self, ast):
        if hasattr(ast, 'linenumber'):
            self.advance_to_line(ast.linenumber)
        self.dispatch.get(type(ast), type(self).print_unknown)(self, ast)

    @dispatch(testast.Python)
    def print_python(self, ast):
        self.indent()
        code = ast.code.source
        if code[0] == '\n':
            self.write("python:")
            with self.increase_indent():
                self.write_lines(split_logical_lines(code[1:]))
        else:
            self.write("$ %s" % code)

    @dispatch(testast.Assert)
    def print_assert(self, ast):
        self.indent()
        self.write('assert %s' % ast.expr)

    @dispatch(testast.Jump)
    def print_jump(self, ast):
        self.indent()
        self.write('jump %s' % ast.target)

    @dispatch(testast.Call)
    def print_call(self, ast):
        self.indent()
        self.write('call %s' % ast.target)

    @dispatch(testast.Action)
    def print_action(self, ast):
        self.indent()
        self.write('run %s' % ast.expr)

    @dispatch(testast.Pause)
    def print_pause(self, ast):
        self.indent()
        self.write('pause %s' % ast.expr)

    @dispatch(testast.Label)
    def print_label(self, ast):
        self.indent()
        self.write('label %s' % ast.name)

    @dispatch(testast.Type)
    def print_type(self, ast):
        self.indent()
        if len(ast.keys[0]) == 1:
            self.write('type "%s"' % string_escape(''.join(ast.keys)))
        else:
            self.write('type %s' % ast.keys[0])
        if ast.pattern is not None:
            self.write(' pattern "%s"' % string_escape(ast.pattern))
        if hasattr(ast, 'position') and ast.position is not None:
            self.write(' pos %s' % ast.position)

    @dispatch(testast.Drag)
    def print_drag(self, ast):
        self.indent()
        self.write('drag %s' % ast.points)
        if ast.button != 1:
            self.write(' button %d' % ast.button)
        if ast.pattern is not None:
            self.write(' pattern "%s"' % string_escape(ast.pattern))
        if ast.steps != 10:
            self.write(' steps %d' % ast.steps)

    @dispatch(testast.Move)
    def print_move(self, ast):
        self.indent()
        self.write('move %s' % ast.position)
        if ast.pattern is not None:
            self.write(' pattern "%s"' % string_escape(ast.pattern))

    @dispatch(testast.Click)
    def print_click(self, ast):
        self.indent()
        if ast.pattern is not None:
            self.write('"%s"' % string_escape(ast.pattern))
        else:
            self.write('click')
        if hasattr(ast, 'button') and ast.button != 1:
            self.write(' button %d' % ast.button)
        if hasattr(ast, 'position') and ast.position is not None:
            self.write(' pos %s' % ast.position)
        if hasattr(ast, 'always') and ast.always:
            self.write(' always')

    @dispatch(testast.Until)
    def print_until(self, ast):
        if hasattr(ast.right, 'linenumber'):
            # We don't have our own line number, and it's not guaranteed that left has a line number.
            # Go to right's line number now since we can't go to it after we print left.
            self.advance_to_line(ast.right.linenumber)
        self.print_node(ast.left)
        self.write(' until ')
        self.skip_indent_until_write = True
        self.print_node(ast.right)