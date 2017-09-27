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

from util import say_get_code
import renpy

import hashlib
import re
from copy import copy

class Translator(object):
    def __init__(self, language, saving_translations=False):
        self.language = language
        self.saving_translations = saving_translations
        self.strings = {}
        self.dialogue = {}
        self.identifiers = set()

    # Adapted from Ren'Py's Restructurer.create_translate
    def create_translate(self, block):
        if self.saving_translations:
            return [] # Doesn't matter, since we're throwing this away in this case

        md5 = hashlib.md5()

        for i in block:
            if isinstance(i, renpy.ast.Say):
                code = say_get_code(i)
            elif isinstance(i, renpy.ast.UserStatement):
                code = i.line
            else:
                raise Exception("Don't know how to get canonical code for a %s" % str(type(i)))
            md5.update(code.encode("utf-8") + b"\r\n")

        if self.label:
            base = self.label + "_" + md5.hexdigest()[:8]
        else:
            base = md5.hexdigest()[:8]

        i = 0
        suffix = ""

        while True:

            identifier = base + suffix

            if identifier not in self.identifiers:
                break

            i += 1
            suffix = "_{0}".format(i)

        self.identifiers.add(identifier)

        translated_block = self.dialogue.get(identifier)
        if translated_block is None:
            return block

        new_block = []
        old_linenumber = block[0].linenumber
        for ast in translated_block:
            new_ast = copy(ast)
            new_ast.linenumber = old_linenumber
            new_block.append(new_ast)
        return new_block

    def walk(self, ast, f):
        if isinstance(ast, (renpy.ast.Init, renpy.ast.Label, renpy.ast.While, renpy.ast.Translate, renpy.ast.TranslateBlock)):
            f(ast.block)
        elif isinstance(ast, renpy.ast.Menu):
            for i in ast.items:
                if i[2] is not None:
                    f(i[2])
        elif isinstance(ast, renpy.ast.If):
            for i in ast.entries:
                f(i[1])

    # Adapted from Ren'Py's Restructurer.callback
    def translate_dialogue(self, children):
        new_children = [ ]
        group = [ ]

        for i in children:

            if isinstance(i, renpy.ast.Label):
                if not (hasattr(i, 'hide') and i.hide):
                    self.label = i.name

            if self.saving_translations and isinstance(i, renpy.ast.TranslateString) and i.language == self.language:
                self.strings[i.old] = i.new

            if not isinstance(i, renpy.ast.Translate):
                self.walk(i, self.translate_dialogue)
            elif self.saving_translations and i.language == self.language:
                self.dialogue[i.identifier] = i.block

            if isinstance(i, renpy.ast.Say):
                group.append(i)
                tl = self.create_translate(group)
                new_children.extend(tl)
                group = [ ]

            elif hasattr(i, 'translatable') and i.translatable:
                group.append(i)

            else:
                if group:
                    tl = self.create_translate(group)
                    new_children.extend(tl)
                    group = [ ]

                new_children.append(i)

        if group:
            nodes = self.create_translate(group)
            new_children.extend(nodes)
            group = [ ]

        children[:] = new_children
