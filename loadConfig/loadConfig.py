import json


class Config:
    def __init__(self, configFile):
        self.file = configFile
        self.data = self._load_conf()

    def _load_conf(self):
        """Load JSON data from the file."""
        try:
            with open(self.file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: The file '{self.file}' was not found.")
            return {}
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON.")
            return {}
