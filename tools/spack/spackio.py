
import os

from typing import Tuple, Optional, List

from spack.spack import Spack, SpackType, SpackDB, trim_to_mod_assets, sprite_paths


class SpackLoader():
    """
    Loads spacks
    """

    # alias
    trim_to_mod_assets = trim_to_mod_assets

    @classmethod
    def load(cls, ma_folder_path: str) -> SpackDB:
        """
        Loads any spacks inside a mod assets folder path
        :param ma_folder_path: mod assets folder path
        :returns: Spack Database
        """
        ma_folder_path = trim_to_mod_assets(ma_folder_path)
        db = SpackDB()

        for path in sprite_paths():
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


class SpackWriter():
    """
    Writes spacks
    """

    # alias
    trim_to_mod_assets = trim_to_mod_assets

    @staticmethod
    def delete_spack(ma_folder_path: str, spack: Spack):
        """
        deletes a spack. Cannot be reversed
        :param spack: spack to delete
        """
        if spack.is_new:
            file_list = [
                path_from_type(spack.spack_type, spack.img_sit, file_name)
                for file_name in spack.file_list
            ]

        else:
            file_list = spack.file_list

        for file_name in file_list:
            real_path = os.path.normcase(os.path.join(ma_folder_path, file_name))
            os.remove(real_path)

    @staticmethod
    def convert_spack(src_spack: Spack, dest_spack: Spack):
        """
        Converts the spack
        :param src_spack: the spack to start with
        :param dest_spack: the spack to convert to
        """