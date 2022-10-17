

from dataclasses import dataclass, field
from collections import defaultdict

from spack.spack import SpackType, SpackStructureType, Spack
from spack.spackjson import SpackJSONDB


def _defaultdict_maker():
    return defaultdict(dict)


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

    # spack jsons
    spacks_json = SpackJSONDB = SpackJSONDB()

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

    def has_jsons(self) -> bool:
        """
        Checks if we have json data
        """
        return len(self.SpackJSONDB) > 0