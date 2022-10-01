
from typing import Optional, Dict, DefaultDict, Tuple, NamedTuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


def _defaultdict_maker():
    return defaultdict(dict)


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


class SpackEntry(NamedTuple):
    old: Optional[Spack] = None
    new: Optional[Spack] = None


@dataclass
class SpackDB():
    """
    Contains spacks
    """

    # spacks organized by type
    spacks_by_type: DefaultDict[SpackType, Dict[str, SpackEntry]] = field(default_factory=_defaultdict_maker)


    def __getitem__(self, item) -> Dict[str, SpackEntry]:
        if item not in (SpackType.ACS, SpackType.HAIR, SpackType.CLOTHES):
            raise ValueError("invalid spack type - {0}".format(item))

        return self.spacks_by_type[item]

    def __len__(self):
        return len(self[SpackType.HAIR]) + len(self[SpackType.ACS]) + len(self[SpackType.CLOTHES])

    def add(self, spack: Spack) -> 'SpackDB':
        """
        Adds a spack to this DB
        :param spack: spack to add
        :returns: self for chaining
        """
        spacks_dict = self[spack.spack_type]
        existing_spack = spacks_dict.get(spack.img_sit, None)

        if existing_spack:
            old_spack, new_spack = existing_spack

            if old_spack == spack:
                old_spack.merge(spack)

            elif new_spack == spack:
                new_spack.merge(spack)

        else:
            # not existing, create new one
            old_spack = None
            new_spack = None

            if spack.is_new:
                new_spack = spack
            else:
                old_spack = spack

            spacks_dict[spack.img_sit] = SpackEntry(old=old_spack, new=new_spack)

        return self