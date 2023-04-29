import os

import enum
from typing import List
from server.generation.jupiter_from_py import create_jupiter

SAMPLE_SRC = "server/generation/samples/sample_work.py"


class GenType(enum.Enum):
    BASE = "BASE"
    NOT_BASE = "NEW"


class NotebookGenerator:
    def __init__(self, prefix, directory):
        self.prefix = prefix
        self.directory = directory

    def generate_notebooks(self, n) -> List[str]:
        self.create_directory_if_needs()
        file_paths = []
        file_names = []

        for i in range(n):
            file_name = f"{self.prefix}_VAR{i}.ipynb"
            file_path = os.path.join(self.directory, file_name)

            create_jupiter(SAMPLE_SRC, file_path)

            file_paths.append(file_path)
            file_names.append(file_name)
        return file_names

    def create_directory_if_needs(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def clear_directory(self):
        if os.path.isdir(self.directory):
            os.rmdir(self.directory)
