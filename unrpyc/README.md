master: [![Build Status](https://travis-ci.org/CensoredUsername/unrpyc.svg?branch=master)]
(https://travis-ci.org/CensoredUsername/unrpyc)

dev: [![Build Status](https://travis-ci.org/CensoredUsername/unrpyc.svg?branch=dev)]
(https://travis-ci.org/CensoredUsername/unrpyc)

Unrpyc is a script to decompile Ren'Py (http://www.renpy.org/) compiled .rpyc
script files. It will not extract files from .rpa archives. For that, use
[rpatool](https://github.com/Shizmob/rpatool) or [UnRPA]
(https://github.com/Lattyware/unrpa).

Thanks to recent changes, unrpyc no longer needs internal renpy structures to
work.

Usage options:

Options:
```
  --version      show program's version number and exit

  -h, --help     show this help message and exit

  -c, --clobber  overwrites existing output files

  -d, --dump     Instead of decompiling, pretty print the contents
                 of the AST in a human readable format.
                 This is mainly useful for debugging.
  -p, --processes
                 use the specified number of processes to decompile
  --sl1-as-python
                 Only dumping and for decompiling screen language 1
                 screens. Convert SL1 Python AST to Python code instead
                 of dumping it or converting it to screenlang.
  --comparable   Only for dumping, remove several false differences when
                 comparing dumps. This suppresses attributes that are
                 different even when the code is identical, such as file
                 modification times.
  --no-pyexpr    Only for dumping, disable special handling of PyExpr objects,
                 instead printing them as strings. This is useful when comparing
                 dumps from different versions of Ren'Py. It should only be used
                 if necessary, since it will cause loss of information such as
                 line numbers.
  --init-offset  Attempt to guess when init offset statements were used and
                 insert them. This is always safe to enable if the game's Ren'Py
                 version supports init offset statements, and the generated code
                 is exactly equivalent, only less cluttered.
```
Usage: [python2] unrpyc.py [options] script1 script2 ...

You can give several .rpyc files on the command line. Each script will be
decompiled to a corresponding .rpy on the same directory. Additionally, you can
pass directories. All .rpyc files in these directories or their subdirectories
will be decompiled. By default, the program will not overwrite existing files,
use -c to do that.

This script will try to disassemble all AST nodes. In the case it encounters an
unknown node type, which may be caused by an update to Ren'Py somewhere in the
future, a warning will be printed and a placeholder inserted in the script when
it finds a node it doesn't know how to handle. If you encounter this, please
open an issue to alert us of the problem.

For the script to run correctly it is required for the unrpyc.py file to be in
the same directory as the modules directory.

You can also import the module from python and call
unrpyc.decompile_rpyc(filename, ...) directly

As of renpy version 6.18 the way renpy handles screen language changed
significantly. Due to this significant changes had to be made, and the script
might be less stable for older renpy versions. If you encounter any problems
due to this, please report them.

Alternatively there is an experimental version of the decompiler packed into
one file available at https://github.com/CensoredUsername/unrpyc/releases
This version will decompile a game from inside the renpy runtime. Simply copy
the un.rpyc file into the "game" directory inside the game files and everything
will be decompiled.

Supported:
* renpy version 6
* Windows, OSX and Linux

Unrpyc has only been tested on versions up to 6.99.9, though newer versions are
expected to mostly work. If you find an error due to a new ren'py version being
incompatible, please open an issue.

Requirements:
* Python version 2.7

https://github.com/CensoredUsername/unrpyc
