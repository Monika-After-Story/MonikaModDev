#!/usr/bin/env python2

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

import argparse
from os import path, walk
import codecs
import glob
import itertools
import traceback
import struct
from multiprocessing import Pool, Lock, cpu_count
from operator import itemgetter

import decompiler
from decompiler import magic, astdump, translate

# special definitions for special classes

class PyExpr(magic.FakeStrict, unicode):
    __module__ = "renpy.ast"
    def __new__(cls, s, filename, linenumber):
        self = unicode.__new__(cls, s)
        self.filename = filename
        self.linenumber = linenumber
        return self

    def __getnewargs__(self):
        return unicode(self), self.filename, self.linenumber

class PyCode(magic.FakeStrict):
    __module__ = "renpy.ast"
    def __setstate__(self, state):
        (_, self.source, self.location, self.mode) = state
        self.bytecode = None

class_factory = magic.FakeClassFactory((PyExpr, PyCode), magic.FakeStrict)

printlock = Lock()

# API

def read_ast_from_file(in_file):
    # .rpyc files are just zlib compressed pickles of a tuple of some data and the actual AST of the file
    raw_contents = in_file.read()
    if raw_contents.startswith("RENPY RPC2"):
        # parse the archive structure
        position = 10
        chunks = {}
        while True:
            slot, start, length = struct.unpack("III", raw_contents[position: position + 12])
            if slot == 0:
                break
            position += 12

            chunks[slot] = raw_contents[start: start + length]

        raw_contents = chunks[1]

    raw_contents = raw_contents.decode('zlib')
    data, stmts = magic.safe_loads(raw_contents, class_factory, {"_ast"})
    return stmts

def decompile_rpyc(input_filename, overwrite=False, dump=False, decompile_python=False,
                   comparable=False, no_pyexpr=False, translator=None, init_offset=False):
    # Output filename is input filename but with .rpy extension
    filepath, ext = path.splitext(input_filename)
    out_filename = filepath + ('.txt' if dump else '.rpy')

    with printlock:
        print "Decompiling %s to %s..." % (input_filename, out_filename)

        if not overwrite and path.exists(out_filename):
            print "Output file already exists. Pass --clobber to overwrite."
            return False # Don't stop decompiling if one file already exists

    with open(input_filename, 'rb') as in_file:
        ast = read_ast_from_file(in_file)

    with codecs.open(out_filename, 'w', encoding='utf-8') as out_file:
        if dump:
            astdump.pprint(out_file, ast, decompile_python=decompile_python, comparable=comparable,
                                          no_pyexpr=no_pyexpr)
        else:
            decompiler.pprint(out_file, ast, decompile_python=decompile_python, printlock=printlock,
                                             translator=translator, init_offset=init_offset)
    return True

def extract_translations(input_filename, language):
    with printlock:
        print "Extracting translations from %s..." % input_filename

    with open(input_filename, 'rb') as in_file:
        ast = read_ast_from_file(in_file)

    translator = translate.Translator(language, True)
    translator.translate_dialogue(ast)
    # we pickle and unpickle this manually because the regular unpickler will choke on it
    return magic.safe_dumps(translator.dialogue), translator.strings

def worker(t):
    (args, filename, filesize) = t
    try:
        if args.write_translation_file:
            return extract_translations(filename, args.language)
        else:
            if args.translation_file is not None:
                translator = translate.Translator(None)
                translator.language, translator.dialogue, translator.strings = magic.loads(args.translations, class_factory)
            else:
                translator = None
            return decompile_rpyc(filename, args.clobber, args.dump, decompile_python=args.decompile_python,
                                  no_pyexpr=args.no_pyexpr, comparable=args.comparable, translator=translator, init_offset=args.init_offset)
    except Exception as e:
        with printlock:
            print "Error while decompiling %s:" % filename
            print traceback.format_exc()
        return False

def sharelock(lock):
    global printlock
    printlock = lock

def main():
    # python27 unrpyc.py [-c] [-d] [--python-screens|--ast-screens|--no-screens] file [file ...]
    parser = argparse.ArgumentParser(description="Decompile .rpyc files")

    parser.add_argument('-c', '--clobber', dest='clobber', action='store_true',
                        help="overwrites existing output files")

    parser.add_argument('-d', '--dump', dest='dump', action='store_true',
                        help="instead of decompiling, pretty print the ast to a file")

    parser.add_argument('-p', '--processes', dest='processes', action='store', default=cpu_count(),
                        help="use the specified number of processes to decompile")

    parser.add_argument('-t', '--translation-file', dest='translation_file', action='store', default=None,
                        help="use the specified file to translate during decompilation")

    parser.add_argument('-T', '--write-translation-file', dest='write_translation_file', action='store', default=None,
                        help="store translations in the specified file instead of decompiling")

    parser.add_argument('-l', '--language', dest='language', action='store', default='english',
                        help="if writing a translation file, the language of the translations to write")

    parser.add_argument('--sl1-as-python', dest='decompile_python', action='store_true',
                        help="Only dumping and for decompiling screen language 1 screens. "
                        "Convert SL1 Python AST to Python code instead of dumping it or converting it to screenlang.")

    parser.add_argument('--comparable', dest='comparable', action='store_true',
                        help="Only for dumping, remove several false differences when comparing dumps. "
                        "This suppresses attributes that are different even when the code is identical, such as file modification times. ")

    parser.add_argument('--no-pyexpr', dest='no_pyexpr', action='store_true',
                        help="Only for dumping, disable special handling of PyExpr objects, instead printing them as strings. "
                        "This is useful when comparing dumps from different versions of Ren'Py. "
                        "It should only be used if necessary, since it will cause loss of information such as line numbers.")

    parser.add_argument('--init-offset', dest='init_offset', action='store_true',
                        help="Attempt to guess when init offset statements were used and insert them. "
                        "This is always safe to enable if the game's Ren'Py version supports init offset statements, "
                        "and the generated code is exactly equivalent, only less cluttered.")

    parser.add_argument('file', type=str, nargs='+',
                        help="The filenames to decompile. "
                        "All .rpyc files in any directories passed or their subdirectories will also be decompiled.")

    args = parser.parse_args()

    if args.write_translation_file and not args.clobber and path.exists(args.write_translation_file):
        # Fail early to avoid wasting time going through the files
        print "Output translation file already exists. Pass --clobber to overwrite."
        return

    if args.translation_file:
        with open(args.translation_file, 'rb') as in_file:
            args.translations = in_file.read()

    # Expand wildcards
    def glob_or_complain(s):
        retval = glob.glob(s)
        if not retval:
            print "File not found: " + s
        return retval
    filesAndDirs = map(glob_or_complain, args.file)
    # Concatenate lists
    filesAndDirs = list(itertools.chain(*filesAndDirs))

    # Recursively add .rpyc files from any directories passed
    files = []
    for i in filesAndDirs:
        if path.isdir(i):
            for dirpath, dirnames, filenames in walk(i):
                files.extend(path.join(dirpath, j) for j in filenames if len(j) >= 5 and j[-5:] == '.rpyc')
        else:
            files.append(i)

    # Check if we actually have files. Don't worry about
    # no parameters passed, since ArgumentParser catches that
    if len(files) == 0:
        print "No script files to decompile."
        return

    files = map(lambda x: (args, x, path.getsize(x)), files)
    processes = int(args.processes)
    if processes > 1:
        # If a big file starts near the end, there could be a long time with
        # only one thread running, which is inefficient. Avoid this by starting
        # big files first.
        files.sort(key=itemgetter(2), reverse=True)
        results = Pool(int(args.processes), sharelock, [printlock]).map(worker, files, 1)
    else:
        # Decompile in the order Ren'Py loads in
        files.sort(key=itemgetter(1))
        results = map(worker, files)

    if args.write_translation_file:
        print "Writing translations to %s..." % args.write_translation_file
        translated_dialogue = {}
        translated_strings = {}
        good = 0
        bad = 0
        for result in results:
            if not result:
                bad += 1
                continue
            good += 1
            translated_dialogue.update(magic.loads(result[0], class_factory))
            translated_strings.update(result[1])
        with open(args.write_translation_file, 'wb') as out_file:
            magic.safe_dump((args.language, translated_dialogue, translated_strings), out_file)

    else:
        # Check per file if everything went well and report back
        good = results.count(True)
        bad = results.count(False)

    if bad == 0:
        print "Decompilation of %d script file%s successful" % (good, 's' if good>1 else '')
    elif good == 0:
        print "Decompilation of %d file%s failed" % (bad, 's' if bad>1 else '')
    else:
        print "Decompilation of %d file%s successful, but decompilation of %d file%s failed" % (good, 's' if good>1 else '', bad, 's' if bad>1 else '')

if __name__ == '__main__':
    main()