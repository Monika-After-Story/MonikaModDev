
import os
import re

from typing import Optional
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


def _defaultdict_maker():
    return defaultdict(dict)


#region file stuff


MOD_ASSETS = "mod_assets"
PNG_EXT = ".png"


# matches old ACS files. 2 capturing groups:
#   1 - acs ID (img sit)
#   2 - ACS file codes
ACS_FILE_IN_OLD = re.compile(r"acs-(\w+)-([\w-]+)\.png")

# output for old ACS files:
#   0 - img_sit
#   1 - ACS file codes
ACS_FILE_OUT_OLD = "acs-{0}-{1}.png"

# matches new ACS files. 1 capturing group:
#   1 - ACS file codes
ACS_FILE_IN_NEW = re.compile(r"(\w+)\.png")

# output for new ACS files:
#   0 - ACS file codes
ACS_FILE_OUT_NEW = "{0}.png"

# matches old hair files. 3 capturing groups:
#   1 - lean type (only if leaning)
#   2 - hair ID (img sit)
#   3 - hair code (front/back/mid/etc...)
#   4 - any remaining hair codes like highlight, will include dash (-) prefix
HAIR_FILE_IN_OLD = re.compile(r"hair-(?:leaning-(\w+)-){0,1}(\w+)-(back|mid|front|0|5|10)((?:-\w+)*)\.png")

# output for old hair files
#   0 - leaning + lean type (only if leaning)
#   1 - hair ID (img sit)
#   2 - hair code (front/back/mid/etc...)
#   3 - any remaining hair codes like highlight, will include dash (-) prefix
HAIR_FILE_OUT_OLD = "hair-{0}{1}-{2}{3}.png"

# matches new hair files.
#   1 - lean type (only if leaning)
#   2 - hair code (front/back/mid/etc...)
#   3 - any remaining hair codes like highlight, will include dash (-) prefix
HAIR_FILE_IN_NEW = re.compile(r"(?:(\w+)-){0,1}(back|mid|front|0|5|10)((?:-\w+)*)\.png")

# output for new hair files
#   0 - lean type (only if leaning)
#   1 - hair code (front/back/mid/etc...)
#   2 - any remaining hair codes like highlight, will include dash (-) prefix
HAIR_FILE_OUT_NEW = "{0}{1}{2}.png"


PATH_PREFIX = "monika/"


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


@dataclass
class ConverterPackage():
    """
    used for file converter to convert between things
    """

    @property
    def img_sit(self):
        """
        Should be the img_sit corresponding data
        """
        raise NotImplemented

    @img_sit.setter
    def img_sit(self, val):
        """
        Should set the img sit data
        """
        raise NotImplemented

@dataclass
class ACSConverterPackage(ConverterPackage):
    """
    ACS converter package
    """
    # ACS ID (img_sit)
    acs_id: str = ""
    # ACS file codes
    file_codes: str = ""

    @property
    def img_sit(self):
        return self.acs_id

    @img_sit.setter
    def img_sit(self, val):
        self.acs_id = val


@dataclass
class HairConverterPackage(ConverterPackage):
    """
    Hair converter package
    """
    # hair ID (img_sit)
    hair_id: str = ""
    # hair code
    hair_code: str = ""
    # other hair codes
    _other_hair_codes: str = ""
    # lean type (if appropriate)
    _lean_type: str = ""

    @property
    def img_sit(self):
        return self.hair_id

    @img_sit.setter
    def img_sit(self, val):
        self.hair_id = val

    @property
    def lean_type(self):
        # lean type (only if leaning)
        return self._lean_type

    @lean_type.setter
    def lean_type(self, val):
        if val is None:
            val = ""
        self._lean_type = val

    @property
    def other_hair_codes(self):
        return self._other_hair_codes

    @other_hair_codes.setter
    def other_hair_codes(self, val):
        if val is None:
            val = ""
        self._other_hair_codes = val


class FileConverter():
    # input pattern for old-style file
    old_input_pattern: re.Pattern[str]

    # output format string for old-style file
    old_output_format: str

    # input pattern for new-style file
    new_input_pattern: re.Pattern[str]

    # output format string for new-style file
    new_output_format: str

    def __init__(self,
        old_input_pattern: re.Pattern[str],
        old_output_format: str,
        new_input_pattern: re.Pattern[str],
        new_output_format: str
    ):
        self.old_input_pattern = old_input_pattern
        self.old_output_format = old_output_format
        self.new_input_pattern = new_input_pattern
        self.new_output_format = new_output_format

    def build_converter_package(self) -> ConverterPackage:
        """
        Create the default converter package here
        :returns: converter package
        """
        return ConverterPackage()

    def create_new_output(self, conv_data: ConverterPackage) -> str:
        """
        Should create a new output string given the conversion data
        :param conv_data: conversion data to create output for
        :returns: new output
        """
        raise NotImplemented

    def create_new_pkg(self, input_str: str, conv_data: ConverterPackage) -> bool:
        """
        Should create new converter package for converter
        :param input_str: input string to create conversion data for
        :param conv_data: conversion data to add to
        :returns: True if input is valid
        """
        raise NotImplemented

    def create_old_output(self, conv_data: ConverterPackage) -> str:
        """
        Should create an old output string given the conversion data
        :param conv_data: conversion data to create output for
        :returns: old output
        """
        raise NotImplemented

    def create_old_pkg(self, input_str: str, conv_data: ConverterPackage) -> bool:
        """
        Should create old converter package for converter
        :param input_str: input string to create conversion data for
        :param conv_data: conversion data to add to
        :returns: True if input is valid
        """
        raise NotImplemented

    def convert_to_new(self, input_str: str, conv_data: ConverterPackage = None) -> str:
        """
        Converts an old str into a new str.
        :param input_str: old input string to convert
        :param conv_data: pass in conversion data if there is data that the input string is missing
        :returns: new output str, or the input str if its not convertable.
        """
        if not conv_data:
            conv_data = self.build_converter_package()

        if self.create_old_pkg(input_str, conv_data):
            return self.create_new_output(conv_data)

        return input_str

    def convert_to_old(self, input_str: str, conv_data: ConverterPackage = None) -> str:
        """
        Converts a new str into an old str
        :param input_str: new input string to convert
        :param conv_data: pass in conversion data if there is data that the input string is missing
        :returns: new output str, or the input str if its not convertable
        """
        if not conv_data:
            conv_data = self.build_converter_package()

        if self.create_new_pkg(input_str, conv_data):
            return self.create_old_output(conv_data)

        return input_str

    def match_on_new(self, input_str: str) -> re.Match:
        """
        Matches on new pattern
        :param input_str: input string to match
        :returns: Match object from match
        """
        return self.new_input_pattern.match(input_str)

    def match_on_old(self, input_str: str) -> re.Match:
        """
        Matches on old pattern
        :param input_str: input string to match
        :returns: Match object from match
        """
        return self.old_input_pattern.match(input_str)


class ACSFileConverter(FileConverter):

    def __init__(self):
        super().__init__(ACS_FILE_IN_OLD, ACS_FILE_OUT_OLD, ACS_FILE_IN_NEW, ACS_FILE_OUT_NEW)

    def build_converter_package(self) -> ConverterPackage:
        return ACSConverterPackage()

    def create_new_output(self, conv_data: ACSConverterPackage) -> str:
        return self.new_output_format.format(conv_data.file_codes)

    def create_old_output(self, conv_data: ACSConverterPackage) -> str:
        return self.old_output_format.format(conv_data.acs_id, conv_data.file_codes)

    def create_new_pkg(self, input_str: str, conv_data: ACSConverterPackage) -> bool:
        match = self.match_on_new(input_str)
        if not match:
            return False

        conv_data.file_codes = match.group(1)
        return True

    def create_old_pkg(self, input_str: str, conv_data: ACSConverterPackage) -> bool:
        match = self.match_on_old(input_str)
        if not match:
            return False

        conv_data.acs_id = match.group(1)
        conv_data.file_codes = match.group(2)
        return True


class HairFileConverter(FileConverter):

    def __init__(self):
        super().__init__(HAIR_FILE_IN_OLD, HAIR_FILE_OUT_OLD, HAIR_FILE_IN_NEW, HAIR_FILE_OUT_NEW)

    def lean_out(self, conv_data: HairConverterPackage) -> str:
        """
        Gets lean out as the appropraite string
        """
        if conv_data.lean_type:
            return conv_data.lean_type + "-"
        return ""

    def build_converter_package(self) -> ConverterPackage:
        return HairConverterPackage()

    def create_new_output(self, conv_data: HairConverterPackage) -> str:
        return self.new_output_format.format(
            self.lean_out(conv_data),
            conv_data.hair_code,
            conv_data.other_hair_codes
        )

    def create_old_output(self, conv_data: HairConverterPackage) -> str:
        return self.old_output_format.format(
            self.lean_out(conv_data),
            conv_data.hair_id,
            conv_data.hair_code,
            conv_data.other_hair_codes
        )

    def create_new_pkg(self, input_str: str, conv_data: HairConverterPackage) -> bool:
        match = self.match_on_new(input_str)
        if not match:
            return False

        conv_data.lean_type = match.group(1)
        conv_data.hair_code = match.group(2)
        conv_data.other_hair_codes = match.group(3)
        return True

    def create_old_pkg(self, input_str: str, conv_data: HairConverterPackage) -> bool:
        match = self.match_on_old(input_str)
        if not match:
            return False

        conv_data.lean_type = match.group(1)
        conv_data.hair_id = match.group(2)
        conv_data.hair_code = match.group(3)
        conv_data.other_hair_codes = match.group(4)
        return True


#endregion


class SpackTypeVerificationResult(Enum):
    INVALID = 0
    OLD = 1
    NEW = 2


class SpackType(Enum):
    ACS = ("a", "acs", ACSFileConverter(), "ACS")
    HAIR = ("h", "hair", HairFileConverter(), "Hair")
    CLOTHES = ("c", None, None, "Clothes")

    # directory name in mod assets structure
    dir_name: str

    # file prefix, if it supports file prefixes.
    # MAY BE NONE if file prefix not supported
    file_prefix: Optional[str]

    # file converter, if it can be converted
    # None if does not support conversion
    file_converter: Optional[FileConverter]

    # display name of this enum
    display_name: str

    def __init__(self, dir_name: str, file_prefix: Optional[str], file_converter: FileConverter, display_name: str):
        """
        ctor
        """
        self.dir_name = dir_name
        self.file_prefix = file_prefix
        self.file_converter = file_converter
        self.display_name = display_name

    def as_dir(self) -> str:
        """
        Converts this enum as if it were a dir. (no trailing slash)
        :returns: value as dir string
        """
        return "/" + self.dir_name

    def as_prefix(self) -> str:
        """
        Converts this enum as if it were a file prefix.
        Does not work for clothes.
        :returns: value as file prefix
        """
        return self.file_prefix

    def as_ma_path(self, *suffixes: str) -> str:
        """
        Converts this enum as a path from mod assets
        :param suffixes: additional elements to add to the path
        :returns: path from mod asseets
        """
        return os.path.join(PATH_PREFIX, self.dir_name, *suffixes)

    def get_img_sit_from_old(self, old_file_name: str) -> Optional[str]:
        """
        Gets image sit from an old file name
        :param old_file_name: old style filename
        :returns: img sit, or null string if could not get
        """
        if self.file_converter:

            old_pkg = self.file_converter.build_converter_package()

            if self.file_converter.create_old_pkg(old_file_name, old_pkg):

                return old_pkg.img_sit

        return None

    def verify_file(self, file_name: str) -> SpackTypeVerificationResult:
        """
        Verifies if the given file is valid for this spack type
        :param file_name: the file name to validate
        :returns: the result of the verification
        """
        if self.file_converter:

            # always try old first, then new
            if self.file_converter.match_on_old(file_name):
                return SpackTypeVerificationResult.OLD

            elif self.file_converter.match_on_new(file_name):
                return SpackTypeVerificationResult.NEW

        return SpackTypeVerificationResult.INVALID

    @classmethod
    def enums(cls) -> list["SpackType"]:
        """
        gets a list of the enum values in here
        :returns: list of enums
        """
        return [x for x in cls]

    @classmethod
    def ma_paths(cls) -> list[str]:
        """
        Gets list of all enums as mod asset paths
        :returns: list of mod asset paths
        """
        return [spack_type.as_ma_path() for spack_type in cls.enums()]

    @classmethod
    def from_path(cls, path: str) -> Optional["SpackType"]:
        """
        determines spack type from the given folder path
        :param path: folder path to check
        :returns: spack type, or None if not valid/unknown spack type
        """
        if path.endswith(cls.ACS.dir_name):
            return cls.ACS

        elif path.endswith(cls.HAIR.dir_name):
            return cls.HAIR

        elif path.endswith(cls.CLOTHES.dir_name):
            return cls.CLOTHES

        return None


class SpackStructureType(Enum):
    FILES = 1
    FOLDER = 2


@dataclass
class Spack():

    # the acutal image id used for the sprites
    img_sit: str

    # how this spack is organized
    structure_type: SpackStructureType

    # list of files associated with this spack
    file_list: list

    # the type of spack this is
    spack_type: SpackType

    def __eq__(self, other: "Spack") -> bool:
        """
        Eq override
        """
        return (
            self.spack_type == other.spack_type
            and self.structure_type == other.structure_type
            and self.img_sit == other.img_sit
        )

    def __ne__(self, other) -> bool:
        """
        ne override
        """
        return not self.__eq__(other)

    @staticmethod
    def menustr(spack: "Spack"):
        """
        Converts spack into menuable string
        """
        return "|".join([
            spack.spack_type.dir_name.capitalize(),
            "N" if spack.structure_type == SpackStructureType.FOLDER else "O",
            spack.img_sit
        ])

    def menu_file_list(self) -> list[str]:
        """
        file list for menu usage
        :returns: list of strings of file names
        """
        if self.structure_type == SpackStructureType.FOLDER:
            return [
                os.path.join(self.img_sit, file_name)
                for file_name in self.file_list
            ]

        return list(self.file_list)


    def merge(self, other: "Spack"):
        """
        Merges the other spack into this one.

        Only merges if same type and structure.
        Raises ValueError if mismatch in type or structure

        :param other: - the other spack to merge
        """
        if self.spack_type != other.spack_type:
            raise ValueError("Failed to merge: Mismatch in spack types")

        if self.structure_type != other.structure_type:
            raise ValueError("Failed to merge: Mismatch in structure")

        if self.img_sit != other.img_sit:
            raise ValueError("Failed to merge: Mismatch in sprite id")

        for file in other.file_list:
            if file not in self.file_list:
                self.file_list.append(file)


class SpackConversion():
    """
    represents a spack conversion that is ready to be executed
    """

    # the spack that is being converted
    src_spack: Spack

    # the resulting spack after conversion
    dest_spack: Spack = None

    # relative file name map - contains tuples of files names with dir prefixes for quick renaming.
    #   [0] - the current file name + dir prefix if needed
    #   [1] - the new file name + dir prefix if needed
    rel_file_name_map: list[tuple[str, str]] = None

    # true if new dir is needed
    needs_dir: bool = False

    # true if this conversion is valid, false if not
    # trying to run conv operations with this when it is invalid should raise exceptions
    is_valid: bool = False

    # the exception that was triggered if this is invalid
    exception: ValueError = None

    def __init__(self, src_spack: Spack):
        self.src_spack = src_spack

        try:
            self.dest_spack, self.rel_file_name_map = SpackConversion._prepare(src_spack)
            self.is_valid = True
            self.needs_dir = self.dest_spack.structure_type == SpackStructureType.FOLDER
        except ValueError as e:
            self.exception = e
            self.is_valid = False

    def __str__(self):
        return "Src: {0}, Dest: {1}, files: {2}".format(self.src_spack, self.dest_spack, self.rel_file_name_map)

    @staticmethod
    def _prepare(src_spack: Spack) -> tuple[Spack, list[tuple[str, str]]]:
        """
        prepares conversion data by processing the current spack for conversion.
        Raises ValueError if incompatible spack, or a file could not be converted
        :param src_spack: the Spack to convert
        :returns: tuple of the following formaT:
            [0] - converted version of this spack
            [1] - list of tuples with filename mappings:
                [0] - current name (includes prefix if needed)
                [1] - name to rename to (includes prefix if needed)
        """
        if src_spack.spack_type == SpackType.CLOTHES:
            raise ValueError("tried to convert unsupported spack: {0}".format(src_spack))

        conv_file_list = []
        conv_name_mapping = []
        conv_data = src_spack.spack_type.file_converter.build_converter_package()
        converting_to_old = src_spack.structure_type == SpackStructureType.FOLDER

        # handling depending on version
        if converting_to_old:
            conv_data.img_sit = src_spack.img_sit

        # convert file names
        for file_name in src_spack.file_list:

            if converting_to_old:
                new_file_name = src_spack.spack_type.file_converter.convert_to_old(file_name, conv_data)
                conv_name_mapping.append((
                    os.path.join(src_spack.img_sit, file_name),
                    new_file_name,
                ))

            else:
                new_file_name = src_spack.spack_type.file_converter.convert_to_new(file_name, conv_data)
                conv_name_mapping.append((
                    file_name,
                    os.path.join(src_spack.img_sit, new_file_name),
                ))

            conv_file_list.append(new_file_name)

            if new_file_name == file_name:
                # this is bad - means no conversion occured
                raise ValueError("file '{0}' did not get converted - check if correctly named".format(file_name))

        return (
            Spack(
                src_spack.img_sit,
                SpackStructureType.FILES if converting_to_old else SpackStructureType.FOLDER,
                conv_file_list,
                src_spack.spack_type
            ),
            conv_name_mapping
        )


@dataclass
class SpackDBFilterCriteria():

    # spack types to filter by
    types: list[SpackType] = None

    # ids to filter by
    ids: list[str] = None

    # structure types to filter by
    struct_types: list[SpackStructureType] = None

    @staticmethod
    def copy(filter_criteria: "SpackDBFilterCriteria") -> "SpackDBFilterCriteria":
        """
        Generates a full copy of filter criteria.
        """
        new_criteria = SpackDBFilterCriteria()

        if filter_criteria.types:
            new_criteria.types = list(filter_criteria.types)
        if filter_criteria.ids:
            new_criteria.ids = list(filter_criteria.ids)
        if filter_criteria.struct_types:
            new_criteria.struct_types = list(filter_criteria.struct_types)

        return new_criteria


@dataclass
class SpackDB():
    """
    Contains spacks
    """

    # spacks organized by type
    spacks_by_type: defaultdict[SpackType, dict[str, dict[SpackStructureType, Spack]]] = field(default_factory=_defaultdict_maker)

    def __getitem__(self, item) -> dict[str, dict[SpackStructureType, Spack]]:
        if item not in SpackType.enums():
            raise ValueError("invalid spack type - {0}".format(item))

        return self.spacks_by_type[item]

    def __len__(self):
        count = 0
        for spack_type in SpackType.enums():
            count += len(self[spack_type])
        return count

    def add(self, spack: Spack) -> 'SpackDB':
        """
        Adds a spack to this DB
        :param spack: spack to add
        :returns: self for chaining
        """
        spacks_dict = self[spack.spack_type]
        existing_spacks = spacks_dict.get(spack.img_sit, None)

        if existing_spacks:
            existing_spack = existing_spacks.get(spack.structure_type)

            if existing_spack:
                existing_spack.merge(spack)

            else:
                # add new one
                existing_spacks[spack.structure_type] = spack

        else:
            # not existing, create new one
            spacks_dict[spack.img_sit] = {
                spack.structure_type: spack
            }

        return self


    def get(
            self,
            types: list[SpackType] = None,
            ids: list[str] = None,
            struct_types: list[SpackStructureType] = None,
            filter_criteria: SpackDBFilterCriteria = None
    ) -> list[Spack]:
        """
        Gets all spacks that pass a specific set of filter criteria. No criteria set will get all spacks in a list.
        :param types: list of types of spack to get
        :param ids: list of ids of the spack to get
        :param struct_types: list of structure types to get
        :param filter_criteria: pass to use objectified filter criteria instead. Takes prioritty.
        :returns: list of spacks
        """
        if filter_criteria:
            types = filter_criteria.types
            ids = filter_criteria.ids
            struct_types = filter_criteria.struct_types

        # defaul types
        if not types:
            types = self.get_types()

        # get base pop of spack ID structures
        spack_id_structs = [self[spack_type] for spack_type in types]

        # apply ID filter
        spack_structures = []
        for spack_id_struct in spack_id_structs:
            if ids:
                for id in ids:
                    spack_structs_from_id = spack_id_struct.get(id)
                    if spack_structs_from_id:
                        spack_structures.append(spack_structs_from_id)
            else:
                spack_structures.extend(list(spack_id_struct.values()))

        # apply struct type filter
        spacks = []
        for spack_struct in spack_structures:
            if struct_types:
                for struct_type in struct_types:
                    spack = spack_struct.get(struct_type)
                    if spack:
                        spacks.append(spack)

            else:
                spacks.extend(list(spack_struct.values()))

        return spacks

    def get_types(self) -> list[SpackType]:
        """
        Gets types that have data in this DB
        :returns: list of SpackTypes
        """
        return [
            spack_type
            for spack_type in SpackType.enums()
            if len(self[spack_type]) > 0
        ]