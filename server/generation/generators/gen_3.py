from typing import List
from server.generation.generators.base import NotebookGenerator, Variant
from server.generation.jupiter_from_py import create_jupiter
from server.tasks.surface import generate_surface_dots
from server.generation.samples import SAMPLE_P3


class Practice_3(NotebookGenerator):
    def __init__(self, prefix):
        self.prefix = prefix

    async def generate_notebooks(self, n) -> List[Variant]:
        variants = []

        for i in range(n):
            file_name = f"{self.prefix}_VAR{i+1}.ipynb"

            notebook = create_jupiter(SAMPLE_P3)

            ind_task = generate_surface_dots()
            cell_idx = len(notebook["cells"]) - 2
            notebook["cells"][cell_idx]["source"] += f"\n\n{ind_task}\n"

            variants.append(Variant(file_name=file_name, notebook=notebook))

        return variants
