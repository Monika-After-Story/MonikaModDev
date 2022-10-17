
import os
import subprocess
import shutil

from typing import Tuple, Optional, List

from spack.spack import Spack, SpackType, SpackDB, trim_to_mod_assets, PNG_EXT,\
    SpackTypeVerificationResult, SpackConversion, SpackStructureType


class SpackLoader():
    """
    Loads spacks
    """

    # path to mod assets folder to check
    ma_folder_path: str

    # databsae of spacks from that mod assets folder
    spack_db: SpackDB

    def __init__(self, ma_folder_path: str):
        self.ma_folder_path = ma_folder_path
        self.spack_db = SpackLoader.load(ma_folder_path)

    def __len__(self):
        return len(self.spack_db)

    def reload(self):
        """
        Reloads this spack's data
        """
        self.spack_db = SpackLoader.load(self.ma_folder_path)

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
            cls._load_path(ma_folder_path, spack_type, db)

        return db

    @classmethod
    def _load_path(cls, ma_folder_path: str, spack_type: SpackType, db: SpackDB):
        """
        Loads spacks in a specific path based on type
        :param ma_folder_path: mod assets folder path
        :param spack_type: the SpackType to get spacks for
        :param db: the DB to load spacks to
        """
        # no clothes for now
        if spack_type == SpackType.CLOTHES:
            return

        sp_folder_path = os.path.normcase(os.path.join(ma_folder_path, spack_type.as_ma_path()))

        # check if this spack has anything of this type
        if not os.access(sp_folder_path, os.F_OK):
            return

        contents = os.listdir(sp_folder_path)
        for file_name in contents:
            spack = cls._try_process_spack(sp_folder_path, file_name)
            if spack:
                db.add(spack)

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

        return Spack(file_name, SpackStructureType.FOLDER, parsed_sub_files, spack_type)

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
            return Spack(img_sit, SpackStructureType.FILES, [file_name], spack_type)

        return None


class SpackWriter():
    """
    Writes spacks
    """

    @classmethod
    def apply_conversion(cls, ma_folder_path: str, spack_conv: SpackConversion, use_git_rename: bool):
        """
        Applies a spack conversion. Throws ValueError if the given spack convesrion data
        is not valid. May throw other errors - see SpackWriter.rename_file

        :param ma_folder_path: the current mod assets folder path
        :param spack_conv: SpackConversion data
        :param use_git_rename: true to use git rename, false if not
        """
        if not spack_conv.is_valid:
            if spack_conv.exception:
                raise spack_conv.exception

            raise ValueError("invalid spack conversion data with no exception: {0}".format(spack_conv))

        ma_folder_path = trim_to_mod_assets(ma_folder_path)

        rel_dir_path = os.path.join(
            ma_folder_path,
            spack_conv.src_spack.spack_type.as_ma_path()
        )

        # make dir if new
        if spack_conv.needs_dir:
            cls.create_dir(os.path.normcase(os.path.join(rel_dir_path, spack_conv.dest_spack.img_sit)))

        # rename files (aka moving)
        for curr, new in spack_conv.rel_file_name_map:
            cls.rename_file(
                os.path.normcase(os.path.join(rel_dir_path, curr)),
                os.path.normcase(os.path.join(rel_dir_path, new)),
                use_git_rename
            )

        # remove dir after if old
        if spack_conv.src_spack.structure_type == SpackStructureType.FOLDER:
            cls.remove_dir(os.path.normcase(os.path.join(rel_dir_path, spack_conv.src_spack.img_sit)))


    @staticmethod
    def create_dir(file_path: str):
        """
        Creates folder for spack (new style)
        """
        try:
            os.mkdir(file_path)
        except FileExistsError:
            pass

    @staticmethod
    def remove_dir(file_path: str):
        """
        Removes folder
        """
        try:
            os.rmdir(file_path)
        except FileNotFoundError:
            pass

    @staticmethod
    def rename_file(cur_name: str, new_name: str, use_git_rename: bool):
        """
        Renames file assuming relative dir.

        If 'use_git_rename' is True, throws CalledProcessError if git rename fails.

        If 'use_git_rename" is False, then the following can occur:
            - on windows, FileExistsError can be raised if file already exists
            - on unix, IsADirectoryError can be raised if the destination file exists as a dir

        Permission errors will also be raised.

        :param cur_name: current name (with path)
        :param new_name: new name (with path)
        :param use_git_rename: true to use git rename, false to not
        """
        if use_git_rename:
            subprocess.run(["git", "mv", cur_name, new_name], shell=True, check=True)

        else:
            shutil.move(cur_name, new_name)












