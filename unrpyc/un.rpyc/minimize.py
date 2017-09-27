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

import ast
import sys
sys.path.append("../decompiler")
from codegen import SourceGenerator

from collections import OrderedDict

# Main API

def minimize(code, remove_docstrings=True, obfuscate_globals=False,
             obfuscate_builtins=False, obfuscate_imports=False):
    # convert the code to an AST
    tree = ast.parse(code)
    if remove_docstrings:
        # optimize the ast by removing docstrings
        tree = DocstringRemover().visit(tree)
    # perform variable name optimization
    tree = ScopeAnalyzer().analyze(
        tree, not obfuscate_globals, not obfuscate_builtins,
        not obfuscate_imports)
    # and now regenerate code from the optimized ast
    return DenseSourceGenerator().process(tree)

# Trimming of unnecessary statements

class DocstringRemover(ast.NodeTransformer):
    def visit_Expr(self, node):
        # Remove any kind of string which does nothing
        if isinstance(node.value, ast.Str):
            return None
        else:
            return self.generic_visit(node)

# Scope analysis implementation

BUILTIN  = 0
MODULE   = 1
CLASS    = 2
FUNCTION = 3

class Scope(object):

    LOCAL    = 1 # It was only written to in this scope
    # LOCAL is a final resolve to this scope
    UNKNOWN  = 2 # It was only read this scope
    # This will resolve to a parent scope if possible, else builtin
    GLOBAL   = 3 # It was declared global in this scope
    # GLOBAL is a final resolve to the global scope
    NONLOCAL = 4 # It was declared nonlocal in this scope
    # This will resolve to a parent scope (but not global)

    def __init__(self, type, protect=False, parent=None):
        # scope type
        self.type = type
        # parent node
        self.parent = parent
        # to get the actual parent scope we need to ignore classes
        while parent and parent.type == CLASS:
            parent = parent.parent
        self.parent_scope = parent
        # names which aren't allowed to be munged in this scope
        self.protect = protect
        self.protected = set()
        # mapping of how scopes are resolved. Before resolving this is a mapping
        # of name: (LOCAL|UNKNOWN|GLOBAL|NONLOCAL), after it is a mapping of
        # name: scope in which the variable lives
        self.resolution = OrderedDict()
        # count of how often a variable is referenced. before resolution this applies
        # to any variables in this scope only, after resolution it counts all references
        # to varialbes which live in this scope
        self.count = {}
        # list of child scopes. Used for recursion while resolving the scopes
        self.children = []
        # Final dict of variables bound to this scope to their munged name. Before munging
        # this is a dict of name: bool(protected), after it is a dict of name: new_name
        self.bound_vars = OrderedDict()

    def child(self, type, protect=False):
        # create a child scope
        child = Scope(type, protect, self)
        self.children.append(child)
        return child

    def read(self, name):
        if name not in self.resolution:
            self.resolution[name] = self.UNKNOWN

        self.count[name] = self.count.get(name, 0) + 1

    def write(self, name, protected=False):
        resolution = self.resolution.get(name, None)
        if resolution is None or resolution == self.UNKNOWN:
            self.resolution[name] = self.LOCAL

        if protected or self.protect:
            self.protected.add(name)

        self.count[name] = self.count.get(name, 0) + 1

    def dec_global(self, name):
        resolution = self.resolution.get(name, None)
        if resolution == self.NONLOCAL:
            raise SyntaxError("name '{0}' is nonlocal and global".format(name))
        else:
            self.resolution[name] = self.GLOBAL

        self.count[name] = self.count.get(name, 0) + 1

    def dec_nonlocal(self, name):
        resolution = self.resolution.get(name, None)
        if resolution == self.GLOBAL:
            raise SyntaxError("name '{0}' is nonlocal and global".format(name))
        else:
            self.resolution[name] = self.NONLOCAL

        self.count[name] = self.count.get(name, 0) + 1

    def resolve_locals(self, global_scope):
        # Resolve anything bound to a known scope
        for name in self.resolution:
            if self.resolution[name] == self.GLOBAL:
                # this variable is bound to the global scope
                self.resolution[name] = global_scope
                # ensure it exists in the global scope
                if name not in global_scope.bound_vars:
                    global_scope.bound_vars[name] = name in self.protected
                else:
                    global_scope.bound_vars[name] |= name in self.protected
                global_scope.count[name] = global_scope.count.get(name, 0) + self.count[name]

            elif self.resolution[name] == self.LOCAL:
                # this variable is bound to this scope
                # Don't have to worry about overwriting protected settings here
                # Since subscopes will be processed later and self.resolution has unique names
                self.bound_vars[name] = name in self.protected
                self.resolution[name] = self
        # recurse
        for scope in self.children:
            scope.resolve_locals(global_scope)

    def resolve_unbounds(self, builtin_scope):
        # and now with all knowns bound, we work out what the rest
        # is bound to
        for name in self.resolution:
            if self.resolution[name] == self.UNKNOWN:
                # look in any sub-scope, else add to builtins
                parent = self.parent_scope
                while parent:
                    if name in parent.bound_vars:
                        self.resolution[name] = parent
                        parent.bound_vars[name] |= name in self.protected
                        parent.count[name] = parent.count.get(name, 0) + self.count[name]
                        break
                    parent = parent.parent_scope
                else:
                    builtin_scope.bound_vars[name] = False
                    builtin_scope.count[name] = builtin_scope.count.get(name, 0) + self.count[name]
                    self.resolution[name] = builtin_scope

            elif self.resolution[name] == self.NONLOCAL:
                # check against any parent-scope but the global scope
                parent = self.parent_scope
                while parent and parent.parent_scope:
                    if name in parent.bound_vars:
                        self.resolution[name] = parent
                        parent.bound_vars[name] |= name in self.protected
                        parent.count[name] = parent.count.get(name, 0) + self.count[name]
                        break
                    parent = parent.parent_scope
                else:
                    raise SyntaxError("no binding for nonlocal '{0}' found".format(
                                      name))
        # recurse
        for scope in self.children:
            scope.resolve_unbounds(builtin_scope)

    def resolve(self, builtin_scope):
        # This is the global scope. Resolve all variables.
        # Assert we're the global scope
        assert self.parent is None
        # This resolves to which scope data is bound (local and global scopes)
        self.resolve_locals(self)
        # This resolves to which scope variables point and returns any found builtin names
        self.resolve_unbounds(builtin_scope)
        return builtin_scope

    def reduce(self, criteria=lambda count, name, protected: count<2 | protected):
        # apply a reduction function to the variables which live in this scope
        # alter the protected status based on the amount of times it was used,
        # its name and if it is protected already
        for name in self.bound_vars:
            self.bound_vars[name] = criteria(self.count[name], name, self.bound_vars[name])

    def munge(self, munger, startval=0):
        # Apply a munger to this scope and any subscopes.
        # a munger is a function which takes a number, zero or higher
        # and generates an unique variable name based those numbers.
        # if a variable in this scope is unprotected, it will be munged
        # otherwise, it will be assigned its name as new name
        for name in self.bound_vars:
            if self.bound_vars[name]:
                self.bound_vars[name] = name
            else:
                self.bound_vars[name] = munger(startval, name)
                startval+= 1

        for scope in self.children:
            scope.munge(munger, startval)

        return startval

def genvarname(number, name):
    rv = []
    while True:
        rv.append(chr(number % 26 + 97))
        number //= 26
        if not number:
            break

    return ''.join(reversed(rv))

class ScopeAnalyzer(ast.NodeTransformer):
    ANALYZE = 1
    # This pass does the work of symtable and some extras
    RENAME = 2
    # The second pass through everything then munges the names

    def __init__(self):
        self.builtin_scope = Scope(BUILTIN)
        self.scope_root = Scope(MODULE)

        self.scope = self.scope_root
        self.stage = None

    def analyze(self, node, protect_globals, protect_builtins, protect_imports, munger=genvarname):
        assert isinstance(node, ast.Module)

        self.protect_imports = protect_imports
        # In this pass we just analyze the variable scopes
        self.stage = self.ANALYZE
        self.generic_visit(node)

        # Resolve all scopes, dumping unresolvable variables in the builtin scope
        self.scope_root.resolve(self.builtin_scope)
        # Use the collected information to resolve variable scopes
        if protect_builtins:
            self.builtin_scope.reduce(lambda count, name, protect: True)
        else:
            self.builtin_scope.reduce(lambda count, name, protect: protect or count<2)
        if protect_globals:
            self.scope_root.reduce(lambda count, name, protect: True)
        else:
            self.scope_root.reduce(lambda count, name, protect: protect or count<2)

        # apply the munger to all variable names,
        val = self.builtin_scope.munge(munger)
        self.scope_root.munge(munger, val)

        # do the rename pass and then add the extra
        # nodes for builtin renaming
        self.stage = self.RENAME
        self.generic_visit(node)

        if not protect_builtins:
            # append the nodes to rename builtins
            extra_nodes = [ast.Assign([ast.Name(value, ast.Store())], ast.Name(key, ast.Load()))
                           for key, value in self.builtin_scope.bound_vars.iteritems() if key != value]
            # ensure any "from __future__ import thing" statements are at the start of the
            futures = [future for future in node.body if
                       isinstance(future, ast.ImportFrom) and future.module == "__future__"]
            # This is technically O(n^2) but from future import statements will always be at the
            # top of a file so it doesn't really matter
            for future in futures:
                node.body.remove(future)
            # put everything back together
            node.body = futures + extra_nodes + node.body
        return node

    def scoped_visit(self, node, type, protect=False):
        # decorators, although they are a part of this node
        # reside in the enclosing scope. so we parse them before and then temporarily
        # empty the decorator_list
        decorators = []
        for decorator in node.decorator_list:
            decorators.append(self.visit(decorator))
        node.decorator_list = []
        if self.stage == self.ANALYZE:
            self.scope = self.scope.child(type, protect)
            node._scope = self.scope
            node = self.generic_visit(node)
            self.scope = self.scope.parent
        else:
            self.scope = node._scope
            node = self.generic_visit(node)
            self.scope = self.scope.parent
            del node._scope
        node.decorator_list = decorators
        return node

    def new_name(self, name):
        # Figure out in which scope the variable is bound
        bound_scope = self.scope.resolution.get(name, self.builtin_scope)
        # And get the new name from that scope
        new_name = bound_scope.bound_vars[name]

        # All names should have been munged by now so this is unnecessary
        if new_name is True:
            return name
        return new_name

    # scope'd nodes

    def visit_Module(self, node):
        # Can be regarded as the actual entry point
        return NotImplementedError("Module scope cannot be nested")

    def visit_ClassDef(self, node):
        if self.stage == self.ANALYZE:
            self.scope.write(node.name, True)
            return self.scoped_visit(node, CLASS, True)
        else:
            node.name = self.new_name(node.name)
            return self.scoped_visit(node, CLASS)

    def visit_FunctionDef(self, node):
        if self.stage == self.ANALYZE:
            self.scope.write(node.name, True)
            return self.scoped_visit(node, FUNCTION)
        else:
            node.name = self.new_name(node.name)
            return self.scoped_visit(node, FUNCTION)

    # name nodes

    def visit_Name(self, node, protected=False):
        if self.stage == self.ANALYZE:
            if isinstance(node.ctx, (ast.Store, ast.AugStore, ast.Param)):
                self.scope.write(node.id, protected)
            else:
                self.scope.read(node.id)
        else:
            node.id = self.new_name(node.id)
        return node

    def visit_NameConstant(self, node):
        if self.stage == self.ANALYZE:
            self.scope.read(repr(node.value))
            return node
        else:
            return ast.Name(self.new_name(repr(node.value)), ast.Load())

    # scope declarations

    def visit_Global(self, node):
        if self.stage == self.ANALYZE:
            for name in node.names:
                self.scope.dec_global(name)
        else:
            for i, name in enumerate(node.names):
                node.names[i] = self.new_name(name)
        return node

    def visit_Nonlocal(self, node):
        # Py3 only
        if self.stage == self.ANALYZE:
            for name in node.names:
                self.scope.dec_nonlocal(name)
        else:
            for i, name in enumerate(node.names):
                node.names[i] = self.new_name(name)
        return node

    # importing

    def visit_Import(self, node):
        for alias in node.names:
            if self.stage == self.ANALYZE:
                self.scope.write(alias.asname or alias.name.split(".", 1)[0], self.protect_imports)
            else:
                if alias.asname:
                    alias.asname = self.new_name(alias.asname)
                else:
                    name = alias.name.split(".", 1)[0]
                    new_name = self.new_name(name)
                    if name != new_name:
                        alias.asname = new_name
        return node

    def visit_ImportFrom(self, node):
        for alias in node.names:
            if self.stage == self.ANALYZE:
                if node.module == "__future__":
                    self.scope.write(alias.name, True)
                elif alias.name == "*":
                    __import__(node.module)
                    mod = sys.modules[node.module]
                    if hasattr(mod, "__all__"):
                        names = mod.__all__
                    else:
                        names = [i for i in mod.__dict__ if not i.startswith("_")]
                    for name in names:
                        self.scope.write(name, True)
                else:
                    self.scope.write(alias.asname or alias.name.split(".", 1)[0], self.protect_imports)
            else:
                if alias.name == "*":
                    pass
                else:
                    if alias.asname:
                        alias.asname = self.new_name(alias.asname)
                    else:
                        name = alias.name.split(".", 1)[0]
                        new_name = self.new_name(name)
                        if name != new_name:
                            alias.asname = new_name
        return node

    # function arguments

    def visit_arguments(self, node):
        if self.stage == self.ANALYZE:
            freelen = len(node.args) - len(node.defaults)
            for i, arg in enumerate(node.args):
                self.visit_Name(arg, i >= freelen)

            for default in node.defaults:
                self.visit(default)

            if node.vararg:
                self.scope.write(node.vararg)
            if node.kwarg:
                self.scope.write(node.kwarg)
        else:
            self.generic_visit(node)
            if node.vararg:
                node.vararg = self.new_name(node.vararg)
            if node.kwarg:
                node.kwarg = self.new_name(node.kwarg)
        return node

# code rewriting implementation

POSSIBLE_WHITESPACE = set([
    " and ",
    " or ",
    " not in ",
    " is not ",
    " in ",
    " is ",
    "not ",
    "if ",
    " if ",
    " else ",
    "elif ",
    "for ",
    " for ",
    "while ",
    "raise ",
    "assert ",
    "return ",
    "with ",
    " as ",
    "exec ",
    "from ",
    " import ",
    "import ",
    "print ",
    "yield ",
])

class DenseSourceGenerator(SourceGenerator):

    COMMA = ","
    COLON = ":"
    ASSIGN = "="
    SEMICOLON = ";"
    ARROW = '->'

    BINOP_SYMBOLS = dict((i, (j.strip(), k)) for i, (j, k)
                         in SourceGenerator.BINOP_SYMBOLS.items())
    CMPOP_SYMBOLS = dict((i, (j.strip(), k))
                         if j not in POSSIBLE_WHITESPACE
                         else (i, (j, k))
                         for i, (j, k)
                         in SourceGenerator.CMPOP_SYMBOLS.items()
                         )

    def __init__(self):
        SourceGenerator.__init__(self, " ", False, False)

    def process(self, node):
        self.new_line = True
        self.visit(node)

        if len(self.result) > 2:
            for i in range(1, len(self.result)-1):
                first = self.result[i]
                last  = self.result[i + 1]
                if (first[-1] == " ") ^ (last[0] == " "):
                    b = int(last[0] == " ")
                    a = b - 2
                    try:
                        if (first[a].isspace() or last[b].isspace()):
                            continue
                    except IndexError:
                        continue

                    if (first[a].isalnum() or first[a] == "_") ^ (last[b].isalnum() or last[b] == "_"):
                        if b == 0:
                            self.result[i] = first[:-1]
                        else:
                            self.result[i+1] = last[1:]

        result = ''.join(self.result)
        self.result = []
        return result

    def write(self, x):
        if not x:
            return

        if not self.indented:
            if self.force_newline:
                self.after_colon = 0
                self.force_newline = False
                self.result.append('\n' + self.indent_with * self.indentation)
            elif self.after_colon == 1:
                self.after_colon = 2
            elif self.result:
                self.result.append(self.SEMICOLON)
            self.indented = True

        self.result.append(x)

    def visit_Str(self, node, frombytes=False):
        self.write(repr(node.s))

    def visit_Module(self, node):
        self.generic_visit(node)

    def newline(self, node=None, extra=0, force=False):
        # ignore extra
        if extra:
            return

        self.indented = False

        if node is None or force:
            self.force_newline = True


    def maybe_break(self, node):
        pass