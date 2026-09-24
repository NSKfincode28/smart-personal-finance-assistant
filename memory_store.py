import json
from pathlib import Path


class ProfileMemoryStore:

    def __init__(self, file_path):
        self.file_path = Path(file_path)

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.file_path.exists():
            self._save({
                "preferences": {}
            })

    def _load(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _save(self, data):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4
            )

    def save_preference(self, name, value):

        data = self._load()

        data["preferences"][name] = value

        self._save(data)

    def get_preferences(self):

        data = self._load()

        return data.get("preferences", {})

    def clear(self):

        self._save({
            "preferences": {}
        })
