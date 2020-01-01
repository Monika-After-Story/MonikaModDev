## TODO
## we need a neato menu for everything
#
# VER: python 2.7

import os
__clean_path = os.getcwd().replace("\\", "/")
if "MonikaModDev/tools" not in __clean_path:
    os.chdir("tools")

try:
    raw_input
except NameError:
    print("run this using py2")
    exit(1)

import spritepuller as spp
import spritechecker as spc
import spritemaker as spm
import testsgenerator as tg
import menutils

menu_main = [
    ("MAS Dev Tools", "Utility: "),
    ("Sprite Puller", spp.run),
    ("Check Sprites", spc.run),
    ("Make Sprites", spm.run),
    ("Generate Expressions Test", tg.run)
]

choice = True

while choice is not None:

    choice = menutils.menu(menu_main)

    if choice is not None:
        choice()

