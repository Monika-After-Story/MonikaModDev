
import os

from typing import Tuple, Optional, List

from spack.spack import Spack, SpackType, SpackDB, trim_to_mod_assets, PNG_EXT,\
    SpackTypeVerificationResult


class SpackLoader():
    """
    Loads spacks
    """

    @classmethod
    def load(cls, ma_folder_path: str) -> SpackDB:
        """
        Loads any spacks inside a mod assets folder path
        :param ma_folder_path: mod assets folder path
        :returns: Spack Database
        """
        ma_folder_path = trim_to_mod_assets(ma_folder_path)
        db = SpackDB()

        for spack_type in SpackType.enums():

            # no clothes for now
            if spack_type != SpackType.CLOTHES:

                sp_folder_path = os.path.normcase(os.path.join(
                    ma_folder_path,
                    spack_type.as_ma_path()
                ))
                contents = os.listdir(sp_folder_path)

                for file_name in contents:
                    spack = cls._try_process_spack(sp_folder_path, file_name)
                    if spack:
                        db.add(spack)

        return db

    @staticmethod
    def parse_file_old(file_name: str) -> Tuple[Optional[SpackType], Optional[str]]:
        """
        Parses a file into its possible spacktype and img sit id
        (assumign old style)
        :param file_name: the file name to parse
        :returns: tuple of the SpackType and img sit id. if either is None, this wasnt a spack.
        """
        if SpackType.ACS.verify_file(file_name) == SpackTypeVerificationResult.OLD:
            return SpackType.ACS, SpackType.ACS.get_img_sit_from_old(file_name)

        elif SpackType.HAIR.verify_file(file_name) == SpackTypeVerificationResult.OLD:
            return SpackType.HAIR, SpackType.HAIR.get_img_sit_from_old(file_name)

        return None, None

    @classmethod
    def _try_process_spack(cls, file_path: str, file_name: str) -> Optional[Spack]:
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
            return cls._try_process_spack_new(fq_name, file_path, file_name)

        elif os.access(fq_name, os.F_OK):
            # not a dir, assume old structure
            return cls._try_process_spack_old(file_name)

        return None

    @staticmethod
    def _try_process_spack_new(fq_name: str, file_path: str, file_name: str) -> Optional[Spack]:
        """
        Tries to process a spack as a new-style spack

        :param fq_name: fully qualified (combined) file name
        :param file_path: path to the file (not including file)
        :param file_name: name of the file
        :returns: the created Spack or None if no valid data
        """
        # check for any actual files
        sub_files = os.listdir(fq_name)
        if not sub_files:
            return None

        # determine type
        spack_type = SpackType.from_path(file_path)
        if not spack_type:
            return None

        # parse all files to fit spack
        parsed_sub_files = []
        for sub_file in sub_files:

            # only keep pngs
            if sub_file.endswith(PNG_EXT):

                if spack_type.verify_file(sub_file) != SpackTypeVerificationResult.NEW:
                    return None # all actual files must be new style

                parsed_sub_files.append(sub_file)

        return Spack(file_name, True, parsed_sub_files, spack_type)

    @classmethod
    def _try_process_spack_old(cls, file_name: str) -> Optional[Spack]:
        """
        Tries to process a spack as an old-style spack

        :param file_name: name of the file
        :returns: the created Spack or None if no valid data
        """
        # determine if spack
        spack_type, img_sit = cls.parse_file_old(file_name)
        if spack_type and img_sit:
            return Spack(img_sit, False, [file_name], spack_type)

        return None


class SpackWriter():
    """
    Writes spacks
    """

    @staticmethod
    def convert_spack(src_spack: Spack, dest_spack: Spack) -> bool:
        """
        Converts the spack
        :param src_spack: the spack to start with
        :param dest_spack: the spack to convert to
        :returns: True on success, false if not
        """
        if src_spack.spack_type == SpackType.CLOTHES:
            return False