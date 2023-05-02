import os

import enum
from typing import List

from server.generation.jupiter_from_py import create_jupiter

SAMPLE_SRC = "server/generation/samples/sample_work.py"


class GenType(enum.Enum):
    BASE = "BASE"
    NOT_BASE = "NEW"


class Variant:
    def __init__(self, file_name, notebook):
        self.file_name = file_name
        self.notebook = notebook
        self.key = None


class NotebookGenerator:
    def __init__(self, prefix, directory):
        self.prefix = prefix
        self.directory = directory

    async def generate_notebooks(self, n) -> List[Variant]:
        self.create_directory_if_needs()
        variants = []

        for i in range(n):
            file_name = f"{self.prefix}_VAR{i}.ipynb"
            file_path = os.path.join(self.directory, file_name)

            notebook = create_jupiter(SAMPLE_SRC)

            variants.append(Variant(file_name=file_name, notebook=notebook))

        return variants

    def create_directory_if_needs(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def clear_directory(self):
        if os.path.isdir(self.directory):
            os.rmdir(self.directory)
