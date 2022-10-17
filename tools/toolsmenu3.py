## TODO
## we need a neato menu for everything
#
# VER: python 3.9.10

import os
__clean_path = os.getcwd().replace("\\", "/")
if "MonikaModDev/tools" not in __clean_path:
    os.chdir("tools")

import spack.spackorganizer as spackorganizer
import menutils3 as menutils
import toolscache

menu_main = [
    ("MAS Dev Tools", "Utility: "),
    ("Spack (Spritepack) Organizer", spackorganizer.run)
]

choice = True

while choice is not None:

    choice = menutils.menu(menu_main)

    if choice is not None:
        choice()

toolscache._save_cache()