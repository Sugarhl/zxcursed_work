import enum
from typing import List

from server.generation.jupiter_from_py import create_jupiter
from server.generation.samples import SAMPLE_SRC


class GenType(enum.Enum):
    BASE = "BASE"
    PRACTICE_1 = "PRACTICE_1"
    PRACTICE_2 = "PRACTICE_2"
    PRACTICE_3 = "PRACTICE_3"
    NOT_BASE = "NEW"


class Variant:
    def __init__(self, file_name, notebook):
        self.file_name = file_name
        self.notebook = notebook
        self.key = None


class NotebookGenerator:
    def __init__(self, prefix):
        self.prefix = prefix

    async def generate_notebooks(self, n) -> List[Variant]:
        variants = []

        for i in range(n):
            file_name = f"{self.prefix}_VAR{i+1}.ipynb"

            notebook = create_jupiter(SAMPLE_SRC)

            variants.append(Variant(file_name=file_name, notebook=notebook))

        return variants
