import json
import shutil
from pathlib import Path
from .singleton import Singleton


class Config(metaclass=Singleton):
    SETTINGS_EXAMPLE_FILE_NAME: str = 'settings.example.json'
    SETTINGS_FILE_NAME: str = 'settings.json'
    data: dict = None

    def __init__(self, filename: str = None):
        self.filename = Config.SETTINGS_FILE_NAME if filename is None else filename

        if not Path(self.filename).is_file():
            shutil.copyfile(self.SETTINGS_EXAMPLE_FILE_NAME, self.filename)

        self.data: dict = self.read(self.filename)

        if self.filename != Config.SETTINGS_EXAMPLE_FILE_NAME:
            self.example: Config = Config(Config.SETTINGS_EXAMPLE_FILE_NAME)

    def version(self) -> str:
        return self.data['version']

    @staticmethod
    def read(filename: str) -> dict:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    def load(self, filename: str):
        self.data = self.read(filename)

    def save(self):
        self.write(self.filename, self.data)

    @staticmethod
    def write(filename: str, data: dict):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4, sort_keys=True)

    def update(self):

        backup_filename: str = f'{self.filename.rstrip(".json")}.{self.version()}.json'
        shutil.copyfile(self.filename, backup_filename)

        # Copy client id to new config file
        outdated: dict = self.data.copy()
        updated: dict = self.example

        # Retain client ID
        updated['client_id'] = outdated['client_id']

        # Transfer formats
        for format_name, format_dictionary in dict(outdated['formats']).items():
            if format_name not in updated['formats']:
                updated['formats'][format_name] = format_dictionary

        self.save()

    def outdated(self) -> bool:
        return self.version() != self.example.version()
