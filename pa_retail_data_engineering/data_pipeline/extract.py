import json

class Extractor:
    """
    responsible for loading a JSON file from a given file path
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        """
        loads and returns the parsed JSON content

        returns:
            dict or list: parsed JSON data
        """
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
