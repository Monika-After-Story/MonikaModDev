

from dataclasses import dataclass, field
from collections import defaultdict
from enum import Enum
from typing import Optional

from spack.spack import SpackType, SpackStructureType, Spack
from spack.spackjson import SpackJSONDB


def _defaultdict_maker():
    return defaultdict(dict)

def _defaultdict_str():
    return defaultdict(str)


@dataclass
class SpackDBFilterCriteria():

    # spack types to filter by
    types: list[SpackType] = None

    # ids to filter by
    ids: list[str] = None

    # structure types to filter by
    struct_types: list[SpackStructureType] = None

    # list of metadata ids to filter by - use only when needed
    metadata_ids: list[int] = None

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
        if filter_criteria.metadata_ids:
            new_criteria.metadata_ids = list(filter_criteria.metadata_ids)

        return new_criteria


class SpackDBLevel(Enum):
    Spack = 0
    MetadataID = 1
    ImgSit = 2
    SpackStructureType = 3
    SpackType = 4


# DB type aliases
SpackMetadataDB = dict[int, Spack]
SpackImgDB = dict[str, SpackMetadataDB]
SpackStructureDB = dict[SpackStructureType, SpackImgDB]
SpackTypeDB = defaultdict[SpackType, SpackStructureDB]


@dataclass
class SpackDB():
    """
    Contains spacks
    """

    # spacks organized by type
    # type -> Structure type -> img_sit -> metadata id: spack
    spacks_by_type: SpackTypeDB = field(default_factory=_defaultdict_maker)

    # spacks organized to get prefix data
    # spack: prefix if necessary
    spack_prefix_db: dict[Spack, str] = field(default_factory=dict)

    # spack jsons
    spacks_json: SpackJSONDB = SpackJSONDB()

    def __len__(self):
        return len(self.spack_prefix_db)

    def add(
            self,
            spack: Spack,
            path_prefix: str = ""
    ) -> 'SpackDB':
        """
        Adds a spack to this DB
        :param spack: spack to add
        :param path_prefix: path prefix if this is not in root dir
        :returns: self for chaining
        """
        # first check in prefix DB for existence
        if spack in self.spack_prefix_db:
            # spack already exists - merge (hash checking should all main vars)
            self._get(spack.spack_type, spack.structure_type, spack.img_sit, spack._metadata_id).merge(spack)

        else:
            # not existing, create new one.
            spacks_dict = self.spacks_by_type[spack.spack_type]

            # check for matching structure
            structure_spacks = spacks_dict.get(spack.structure_type, None)
            if not structure_spacks:
                structure_spacks = {}
                spacks_dict[spack.structure_type] = structure_spacks

            # check for matching img sit
            img_spacks = structure_spacks.get(spack.img_sit, None)
            if not img_spacks:
                img_spacks = {}
                structure_spacks[spack.img_sit] = img_spacks

            # no new structure created here - no need to check for existence first
            img_spacks[spack._metadata_id] = spack

            # lastly add to prefix map
            self.spack_prefix_db[spack] = path_prefix

        return self

    def _filter_pass(self, db_list: list[dict], ids_to_filter: Optional[list]) -> list:
        """
        given a list of dbs, and a list of keys for data in those dbs, generate a list of the data in the list of dbs
        that matches the list of keys.
        :param db_list: list of dbs to filter
        :param ids_to_filter: list of keys of data to keep. If none, all data is kept, so this is basically flattened
        :returns: list of data, filtered if needed
        """
        output = []
        if ids_to_filter:
            for db in db_list:
                for id in ids_to_filter:
                    data = db.get(id)
                    if data:
                        output.append(data)
        else:
            for db in db_list:
                output.extend(db.values())

        return output

    def _get(
            self,
            spack_type: SpackType,
            structure_type: SpackStructureType,
            img_sit: str,
            metadata_id: int = 0
    ) -> Optional[Spack]:
        """
        Gets a single item from the main spack DB - always use this to retrieve a single item.
        :param spack_type: SpackType of spack to get
        :param structure_type: SpackStructureType of spack to get
        :param img_sit: img_sit of spack to get
        :param metadata_id: metadata id of spack to get. Defaults to 0
        :returns: spack, or None if could not get
        """
        return self.spacks_by_type.get(spack_type, {}).get(structure_type, {}).get(img_sit, {}).get(metadata_id, None)

    def get(self, filter_criteria: SpackDBFilterCriteria = None) -> list[Spack]:
        """
        Gets all spacks that pass a specific set of filter criteria. No criteria set will get all spacks in a list.
        :param filter_criteria: critera to filter spacks with
        :returns: list of spacks
        """
        if filter_criteria:
            types = filter_criteria.types
            ids = filter_criteria.ids
            struct_types = filter_criteria.struct_types
            metadata_ids = filter_criteria.metadata_ids
        else:
            types = None
            ids = None
            struct_types = None
            metadata_ids = None

        # default types
        if not types:
            types = self.get_types()

        # get structure dbs
        struct_dbs = [
            self.spacks_by_type[spack_type]
            for spack_type in types
        ]

        # get img_sit dbs
        img_sit_dbs: list[SpackImgDB] = self._filter_pass(struct_dbs, struct_types)

        # get metadata dbs
        metadata_dbs: list[SpackMetadataDB] = self._filter_pass(img_sit_dbs, ids)

        # now get data
        data: list[Spack] = self._filter_pass(metadata_dbs, metadata_ids)
        return data

    def get_types(self) -> list[SpackType]:
        """
        Gets types that have data in this DB
        :returns: list of SpackTypes
        """
        return [
            spack_type
            for spack_type in SpackType.enums()
            if len(self.spacks_by_type[spack_type]) > 0
        ]

    def has_jsons(self) -> bool:
        """
        Checks if we have json data
        """
        return len(self.spacks_json) > 0