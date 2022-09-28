# organizes spritepacks (or regular sprites)
#
# VER: python 3.9.10

import os
import subprocess
import shutil

from typing import Dict, Union, Optional
from dataclasses import dataclass
from enum import Enum

import menutils

use_git_rename = "GIT_MV" in os.environ

PNG_EXT = ".png"


class SpackType(Enum):
    ACS = ("a", "acs")
    HAIR = ("h", "hair")
    CLOTHES = ("c", None)

    # directory name in mod assets structure
    dir_name: str

    # file prefix, if it supports file prefixes.
    # MAY BE NONE if file prefix not supported
    file_prefix: Optional[str]

    def __init__(self, dir_name: str, file_prefix: Optional[str]):
        """
        ctor
        :param dir_name: directory name
        :param file_prefix: file prefix
        """
        self.dir_name = dir_name
        self.file_prefix = file_prefix

    def as_dir(self) -> str:
        """
        Converts this enum as if it were a dir. (no trailing slash)
        :returns: value as dir string
        """
        return "/" + self.value

    def as_prefix(self) -> str:
        """
        Converts this enum as if it were a file prefix.
        Does not work for clothes.
        :returns: value as file prefix
        """
        return self.file_prefix

    @classmethod
    def from_file(cls, file_name: str) -> Optional["SpackType"]:
        """
        determines spack type from the given file name
        :param file_name: file name to check
        :returns: spack type, or None if not valid/unknown spack type
        """
        if file_name.startswith(cls.ACS.as_prefix()):
            return cls.ACS

        elif file_name.startswith(cls.HAIR.as_prefix()):
            return cls.HAIR

        return None

    @classmethod
    def from_path(cls, path: str) -> Optional["SpackType"]:
        """
        determines spack type from the given folder path
        :param path: folder path to check
        :returns: spack type, or None if not valid/unknown spack type
        """
        if path.endswith(cls.ACS.as_dir()):
            return cls.ACS

        elif path.endswith(cls.HAIR.as_dir()):
            return cls.HAIR

        elif path.endswith(cls.CLOTHES.as_dir()):
            return cls.CLOTHES

        return None


@dataclass
class Spack():

    # the acutal image id used for the sprites
    img_sit: str

    # true if organized in new folder structure, false otherwise
    is_new: bool

    # list of files associated with this spack
    file_list: list

    # the type of spack this is
    spack_type: SpackType

    def __eq__(self, other: "Spack") -> bool:
        """
        Eq override
        """
        return self.spack_type == other.spack_type and self.is_new == other.is_new and self.img_sit == other.img_sit

    def __ne__(self, other) -> bool:
        """
        ne override
        """
        return not self.__eq__(other)

    def merge(self, other: "Spack"):
        """
        Merges the other spack into this one.

        Only merges if same type and structure.
        Raises ValueError if mismatch in type or structure

        :param other: - the other spack to merge
        """
        if self.spack_type != other.spack_type:
            raise ValueError("Failed to merge: Mismatch in spack types")

        if self.is_new != other.is_new:
            raise ValueError("Failed to merge: Mismatch in structure")

        if self.img_sit != other.img_sit:
            raise ValueError("Failed to merge: Mismatch in sprite id")

        for file in other.file_list:
            if file not in self.file_list:
                self.file_list.append(file)


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

    def _try_process_spack(self, file_path: str, file_name: str) -> Spack:
        """
        Tries to process the given file (or directory) into its associated spack.
        This does a best guess based on the "file", path, name, and other factors.

        :param file_path: path to the file (not including file)
        :param file_name: name of the file
        :returns: the created Spritepack, or None if no valid data could be processed
        """
        fq_name = os.path.normcase(os.path.join(file_path, file_name))

        if os.path.isdir(fq_name):
            # this is a dir, which means assume new structure

            # check for any actual files
            sub_files = os.listdir(fq_name)
            if sub_files:
                # only keep pngs
                sub_files = [x for x in sub_files if x.endswith(PNG_EXT)]

                # determine type
                spack_type = SpackType.from_path(file_path)

                if spack_type:
                    return Spack(file_name, True, sub_files, spack_type)

        elif os.access(fq_name, os.F_OK):
            # not a dir, assume old structure

            # determine for type
            spack_type = SpackType.from_file(file_name)

            if spack_type:
                # piece out the img sit
                pass

        return None

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
