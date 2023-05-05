import os


from typing import List
from server.generation.base import NotebookGenerator, Variant

from server.generation.jupiter_from_py import create_jupiter
from server.generation.linear import generate_linear_system_latex


SAMPLE_P1 = "server/generation/samples/sample_P1"


class Practice_1(NotebookGenerator):
    def __init__(self, prefix, directory):
        self.prefix = prefix
        self.directory = directory

    async def generate_notebooks(self, n) -> List[Variant]:
        variants = []

        for i in range(n):
            file_name = f"{self.prefix}_VAR{i+1}.ipynb"

            notebook = create_jupiter(SAMPLE_P1)

            ind_task = generate_linear_system_latex()
            cell_idx = len(notebook["cells"]) - 2
            notebook["cells"][cell_idx]["source"] += f"\n \n {ind_task}\n"

            variants.append(Variant(file_name=file_name, notebook=notebook))

        return variants

    def create_directory_if_needs(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def clear_directory(self):
        if os.path.isdir(self.directory):
            os.rmdir(self.directory)
