# Copyright (c) 2013 CensoredUsername
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
import inspect
import codegen
import ast as py_ast
import renpy

def pprint(out_file, ast, decompile_python=False, comparable=False, no_pyexpr=False):
    # The main function of this module, a wrapper which sets
    # the config and creates the AstDumper instance
    AstDumper(out_file, decompile_python=decompile_python, comparable=comparable, no_pyexpr=no_pyexpr).dump(ast)

class AstDumper(object):
    """
    An object which handles the walking of a tree of python objects
    it will create a human-readable representation of all interesting
    attributes and write this to a given stream
    """
    MAP_OPEN = {list: '[', tuple: '(', set: '{', frozenset: 'frozenset({'}
    MAP_CLOSE = {list: ']', tuple: ')', set: '}', frozenset: '})'}

    def __init__(self, out_file=None, decompile_python=False, no_pyexpr=False,
                 comparable=False, indentation=u'    '):
        self.indentation = indentation
        self.out_file = out_file or sys.stdout
        self.decompile_python = decompile_python
        self.comparable = comparable
        self.no_pyexpr = no_pyexpr

    def dump(self, ast):
        self.indent = 0
        self.passed = [] # We'll keep a stack of objects which we've traversed here so we don't recurse endlessly on circular references
        self.print_ast(ast)

    def print_ast(self, ast):
        # Decides which function should be used to print the given ast object.
        if ast in self.passed:
            self.print_other(ast)
            return
        self.passed.append(ast)
        if isinstance(ast, (list, tuple, set, frozenset)):
            self.print_list(ast)
        elif isinstance(ast, renpy.ast.PyExpr):
            self.print_pyexpr(ast)
        elif isinstance(ast, dict):
            self.print_dict(ast)
        elif isinstance(ast, (str, unicode)):
            self.print_string(ast)
        elif isinstance(ast, (int, bool)) or ast is None:
            self.print_other(ast)
        elif inspect.isclass(ast):
            self.print_class(ast)
        elif isinstance(ast, object):
            self.print_object(ast)
        else:
            self.print_other(ast)
        self.passed.pop()

    def print_list(self, ast):
        # handles the printing of simple containers of N elements.
        self.p(self.MAP_OPEN[ast.__class__])

        self.ind(1, ast)
        for i, obj in enumerate(ast):
            self.print_ast(obj)
            if i+1 != len(ast):
                self.p(',')
                self.ind()
        self.ind(-1, ast)
        self.p(self.MAP_CLOSE[ast.__class__])

    def print_dict(self, ast):
        # handles the printing of dictionaries
        self.p('{')

        self.ind(1, ast)
        for i, key in enumerate(ast):
            self.print_ast(key)
            self.p(': ')
            self.print_ast(ast[key])
            if i+1 != len(ast):
                self.p(',')
                self.ind()
        self.ind(-1, ast)
        self.p('}')

    def should_print_key(self, ast, key):
        if key.startswith('_') or not hasattr(ast, key) or inspect.isroutine(getattr(ast, key)):
            return False
        elif not self.comparable:
            return True
        elif key == 'serial':
            ast.serial = 0
        elif key == 'col_offset':
            ast.col_offset = 0 # TODO maybe make this match?
        elif key == 'name' and type(ast.name) == tuple:
            name = ast.name[0]
            if isinstance(name, unicode):
                name = name.encode('utf-8')
            ast.name = (name.split(b'/')[-1], 0, 0)
        elif key == 'location' and type(ast.location) == tuple:
            if len(ast.location) == 4:
                ast.location = (ast.location[0].split('/')[-1].split('\\')[-1], ast.location[1], ast.location[2], 0)
            elif len(ast.location) == 3:
                ast.location = (ast.location[0].split('/')[-1].split('\\')[-1], ast.location[1], 0)
            elif len(ast.location) == 2:
                ast.location = (ast.location[0].split('/')[-1].split('\\')[-1], ast.location[1])
        elif key == 'loc' and type(ast.loc) == tuple:
            ast.loc = (ast.loc[0].split('/')[-1].split('\\')[-1], ast.loc[1])
        elif key == 'filename':
            ast.filename = ast.filename.split('/')[-1].split('\\')[-1]
        elif (key == 'parameters' and ast.parameters is None and
            isinstance(ast, renpy.screenlang.ScreenLangScreen)):
            # When no parameters exist, some versions of Ren'Py set parameters
            # to None and some don't set it at all.
            return False
        elif (key == 'hide' and ast.hide == False and
            (isinstance(ast, renpy.ast.Python) or
            isinstance(ast, renpy.ast.Label))):
            # When hide isn't set, some versions of Ren'Py set it to False and
            # some don't set it at all.
            return False
        elif (key == 'attributes' and ast.attributes is None and
            isinstance(ast, renpy.ast.Say)):
            # When no attributes are set, some versions of Ren'Py set it to None
            # and some don't set it at all.
            return False
        elif (key == 'block' and ast.block == [] and
            isinstance(ast, renpy.ast.UserStatement)):
            # When there's no block, some versions of Ren'Py set it to None
            # and some don't set it at all.
            return False
        elif (key == 'store' and ast.store == 'store' and
            isinstance(ast, renpy.ast.Python)):
            # When a store isn't specified, some versions of Ren'Py set it to
            # "store" and some don't set it at all.
            return False
        elif key == 'translatable' and isinstance(ast, renpy.ast.UserStatement):
            # Old versions of Ren'Py didn't have this attribute, and it's not
            # controllable from the source.
            return False
        elif key == 'hotspot' and isinstance(ast, renpy.sl2.slast.SLDisplayable):
            # Old versions of Ren'Py didn't have this attribute, and it's not
            # controllable from the source.
            return False
        return True

    def print_object(self, ast):
        # handles the printing of anything unknown which inherts from object.
        # prints the values of relevant attributes in a dictionary-like way
        # it will not print anything which is a bound method or starts with a _
        self.p('<')
        self.p(str(ast.__class__)[8:-2] if hasattr(ast, '__class__')  else str(ast))

        if isinstance(ast, py_ast.Module) and self.decompile_python:
            self.p('.code = ')
            self.print_ast(codegen.to_source(ast, unicode(self.indentation)))
            self.p('>')
            return

        keys = list(i for i in dir(ast) if self.should_print_key(ast, i))
        if keys:
            self.p(' ')
        self.ind(1, keys)
        for i, key in enumerate(keys):
            self.p('.')
            self.p(str(key))
            self.p(' = ')
            self.print_ast(getattr(ast, key))
            if i+1 != len(keys):
                self.p(',')
                self.ind()
        self.ind(-1, keys)
        self.p('>')

    def print_pyexpr(self, ast):
        if not self.no_pyexpr:
            self.print_object(ast)
            self.p(' = ')
        self.print_string(ast)

    def print_class(self, ast):
        # handles the printing of classes
        self.p('<class ')
        self.p(str(ast)[8:-2])
        self.p('>')

    def print_string(self, ast):
        # prints the representation of a string. If there are newlines in this string,
        # it will print it as a docstring.
        if b'\n' in ast:
            astlist = ast.split(b'\n')
            if isinstance(ast, unicode):
                self.p('u')
            self.p('"""')
            self.p(self.escape_string(astlist.pop(0)))
            for i, item in enumerate(astlist):
                self.p('\n')
                self.p(self.escape_string(item))
            self.p('"""')
            self.ind()

        else:
            self.p(repr(ast))

    def escape_string(self, string):
        # essentially the representation of a string without the surrounding quotes
        if isinstance(string, unicode):
            return repr(string)[2:-1]
        elif isinstance(string, str):
            return repr(string)[1:-1]
        else:
            return string

    def print_other(self, ast):
        # used as a last fallback and to print things when a recursive lookup is detected
        self.p(repr(ast))

    def ind(self, diff_indent=0, ast=None):
        # print a newline and indent. diff_indent represents the difference in indentation
        # compared to the last line. it will chech the length of ast to determine if it
        # shouldn't indent in case there's only one or zero objects in this object to print
        if ast is None or len(ast) > 1:
            self.indent += diff_indent
            self.p(u'\n' + self.indentation * self.indent)

    def p(self, string):
        # write the string to the stream
        self.out_file.write(unicode(string))