# organizes spritepacks (or regular sprites)
#
# VER: python 3.9.10

import os

from typing import Union

import menutils3 as menutils


from spack.spack import Spack, SpackDB
from spack.spackio import SpackLoader

use_git_rename = "GIT_MV" in os.environ



class SpackConverter():
    """
    Utility class for converting sprites between versions
    """

    # path to mod_assets folder to check
    ma_folder_path: str

    spack_db: SpackDB

    def __init__(self, ma_folder_path: str):
        self.ma_folder_path = ma_folder_path

    def load(self):
        """
        Loads spritepacks in the set dir
        """
        self.spack_db = SpackLoader.load(self.ma_folder_path)






def conv_new(loaded_spacks: SpackLoader):
    pass


def conv_old(loaded_spacks: SpackLoader):
    pass


def show_list(loaded_spacks: SpackLoader):
    """
    Shows list of spacks
    """
    menutils.paginate(
        "Loaded Spacks",
        # TODO
    )


def run():
    """
    Runs spack organizer
    """
    ma_folder = input("enter path to mod assets folder")
    ma_folder = os.path.normcase(ma_folder)
    os.chdir(ma_folder)

    folders = os.listdir()
    if "mod_assets" not in folders:
        print("no mod_assets folder found, quitting...")
        exit(1)

    loaded_spacks = SpackLoader(ma_folder)

    choice = True

    while choice is not None:
        choice = menutils.menu(menu_main)

        if choice is not None:
            choice(loaded_spacks)


menu_main = [
    ("Spack Organizer", "Utility: "),
    ("Show list of Spacks", show_list),
    ("Convert to Folder Structure (New)", conv_new),
    ("Convert to File Structure (Old)", conv_old),
]
