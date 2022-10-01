# organizes spritepacks (or regular sprites)
#
# VER: python 3.9.10

import os
import subprocess
import shutil

from typing import Dict, Union, Optional

import menutils


from spack.spack import Spack, SpackType

use_git_rename = "GIT_MV" in os.environ



class SpackConverter():
    """
    Utility class for converting sprites between versions
    """

    # path to mod_assets folder to check
    ma_folder_path: str

    spacks: Dict[str, Spack]
    spacks_by_type: Dict[SpackType, Dict[str, Spack]]

    def __init__(self, ma_folder_path: str):
        self.ma_folder_path = ma_folder_path

    #region loading



    def load(self):
        """
        Loads spritepacks in the set dir
        """


    #endregion

    def create_dir(self, spack: Spack):
        """
        Creates folder for spack (new style)
        :param spack: Spritepack to create folder for
        """
        try:
            os.mkdir(spack.img_sit)
        except FileExistsError:
            pass

    def rename_file(self, cur_name: str, new_name: str):
        """
        Renames file assuming relative dir
        :param cur_name: current name (with path)
        :param new_name: new name (with path)
        """
        if use_git_rename:
            subprocess.run(["git", "mv", cur_name, new_name], shell=True, check=True)

        else:
            shutil.move(cur_name, new_name)

    def convert_to_new(self, spack: Union[str, Spack]):
        """
        Converts a spack to new (based on string id)
        :param spack: either string id or the spack to convert
        """
        if isinstance(spack, str):
            spack = self.spacks[spack]

        if not isinstance(spack, Spack):
            raise ValueError("expected Spack, got {0}".format(type(spack)))

        for





def conv_new(convert: SpackConverter):
    pass


def conv_old(convert: SpackConverter):
    pass


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

    converter = SpackConverter(ma_folder)

    choice = True

    while choice is not None:
        choice = menutils.menu(menu_main)

        if choice is not None:
            choice(converter)


menu_main = [
    ("Spack Organizer", "Utility: "),
    ("Convert to Folder Structure (New)", conv_new),
    ("Convert to File Structure (Old)", conv_old),
]
