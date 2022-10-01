
import os
import re

from typing import Tuple, Optional

from spack.spack import Spack, SpackType, SpackDB


MOD_ASSETS = "mod_assets"
PNG_EXT = ".png"

ACS_PATH = "monika/a"
HAIR_PATH = "monika/h"
CLOTHES_PATH = "monika/c"
SPRITE_PATHS = [ACS_PATH, HAIR_PATH, CLOTHES_PATH]


# matches ACS files. 2 capturing groups:
#   1 - acs ID (img sit)
#   2 - ACS file codes
ACS_FILE_IN = re.compile(r"acs-(\w+)-([\w-]+)\.png")
ACS_FILE_OUT = "acs-{0}-{1}.png"

# matches non-leaning hair files. 3 capturing groups:
#   1 - hair ID (img sit)
#   2 - hair code (front/back/mid/etc...)
#   3 - any remaining hair codes like highlight, will include dash (-) prefix
HAIR_FILE_IN = re.compile(r"hair-(\w+)-(back|mid|front|0|5|10)((?:-\w+)*)\.png")
HAIR_FILE_OUT = "hair-{0}-{1}{2}.png"

# matches leaning hair files. 4 capturing groups:
#   1 - lean type
#   2 - hair ID (img sit)
#   2 - hair code (front/back/mid/etc...)
#   3 - any remaining hair codes like highlight, will include dash (-) prefix
HAIR_LEAN_FILE_IN = re.compile(r"hair-leaning-(\w+)-(\w+)-(back|mid|front|0|5|10)((?:-\w+)*)\.png")
HAIR_LEAN_FILE_OUT = "hair-leaning-{0}-{1}-{2}{3}.png"


class SpackLoader():
    """
    Loads spacks
    """

    @staticmethod
    def trim_to_mod_assets(ma_folder_path: str) -> str:
        """
        Slices the given ma folder path so the path ends at mod assets.
        Raises exception if not mod assets folder path.
        :param ma_folder_path: mod assets folder path to trim
        :returns: trimmed mod assets folder path
        """
        start = ma_folder_path.find(MOD_ASSETS)
        if start >= 0:
            return ma_folder_path[:start+len(MOD_ASSETS)]

        raise ValueError("mod_assets not in selected folder path: {0}".format(ma_folder_path))

    @classmethod
    def load(cls, ma_folder_path: str) -> SpackDB:
        """
        Loads any spacks inside a mod assets folder path
        :param ma_folder_path: mod assets folder path
        :returns: Spack Database
        """
        ma_folder_path = cls.trim_to_mod_assets(ma_folder_path)
        db = SpackDB()

        for path in SPRITE_PATHS:
            sp_folder_path = os.path.normcase(os.path.join(ma_folder_path, path))
            contents = os.listdir(sp_folder_path)

            for file_name in contents:
                spack = cls._try_process_spack(sp_folder_path, file_name)
                if spack:
                    db.add(spack)

        return db

    @staticmethod
    def parse_file(file_name: str) -> Tuple[Optional[SpackType], Optional[str]]:
        """
        Parses a file into its possible spacktype and img sit id
        :param file_name: the file name to parse
        :returns: tuple of the SpackType and img sit id. if either is None, this wasnt a spack.
        """
        match = ACS_FILE_IN.match(file_name)
        if match:
            # this is acs
            return SpackType.ACS, match.group(1)

        match = HAIR_LEAN_FILE_IN.match(file_name)
        if match:
            # this is leaning hair
            return SpackType.HAIR, match.group(2)

        match = HAIR_FILE_IN.match(file_name)
        if match:
            # this is regular hair
            return SpackType.HAIR, match.group(1)

        return None, None

    @staticmethod
    def _try_process_spack(file_path: str, file_name: str) -> Optional[Spack]:
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

            # determine if spack
            spack_type, img_sit = SpackLoader.parse_file(file_name)
            if spack_type and img_sit:
                return Spack(img_sit, False, [file_name], spack_type)


        return None
