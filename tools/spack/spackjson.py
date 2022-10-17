
import json
import os

from typing import Optional


class SpackJSONDB():

    # mapping of name to json data
    db: dict[str, dict]

    # mapping of img sit + spack type (json val), to name
    img_sit_index: dict[tuple[str, int], str]

    # mapping of name to fq path + filename
    file_db: dict[str, str]

    def __init__(self):
        self.db = {}
        self.img_sit_index = {}
        self.file_db = {}

    def __len__(self):
        return len(self.db)

    def load(self, json_path: str):
        """
        Loads all jsons in a json folder path
        """
        for file_name in os.listdir(json_path):
            if file_name.endswith(".json"):
                self._load_json(os.path.normcase(os.path.join(
                    json_path,
                    file_name
                )))

    def _load_json(self, fq_json_file: str):
        """
        Loads a json from a specific file into the DB
        """
        try:
            with open(fq_json_file, "r") as json_file:
                data = json.load(json_file)
                name = data.get("name")
                img_sit = data.get("img_sit")
                spack_type = data.get("type")
                spack_type_num = int(spack_type)

                if name and img_sit and spack_type is not None:
                    self.db[name] = data
                    self.file_db[name] = fq_json_file
                    self.img_sit_index[(img_sit, spack_type_num)] = name

        except (json.JSONDecodeError, ValueError):
            pass

    def exists(self, img_sit_type: tuple[str, int]) -> bool:
        """
        Checks if data exists
        """
        return img_sit_type in self.img_sit_index

    def get(self, img_sit_type: tuple[str, int]) -> Optional[dict]:
        """
        gets data
        """
        name = self.img_sit_index.get(img_sit_type)
        if not name:
            return None

        return self.db.get(name)

    def get_file(self, img_sit_type: tuple[str, int]) -> str:
        """
        gest file name
        """
        name = self.img_sit_index.get(img_sit_type)
        if not name:
            return ""
        return self.file_db.get(name, "")

    def save(self, name: str = None, img_sit_type: tuple[str, int] = None):
        """
        Saves json for specific img sit data
        :param name: name to save json for.
        :param img_sit_type: img sit type tuple to save data for. Takes priority
        """
        if img_sit_type:
            name = self.img_sit_index.get(img_sit_type)

        if not name:
            return

        fq_json_file = self.file_db.get(name)
        data = self.db.get(name)
        if not fq_json_file or not data:
            return

        with open(fq_json_file, "w") as json_file:
            json.dump(data, json_file, indent=4)