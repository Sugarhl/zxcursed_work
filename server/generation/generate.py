import os
from typing import List


from server.generation.generators.base import GenType, NotebookGenerator, Variant
from server.generation.generators.gen_1 import Practice_1
from server.generation.generators.gen_2 import Practice_2
from server.generation.generators.gen_3 import Practice_3
from server.models.lab import Lab
from server.models.group import Group
from server.models.student import Student
from server.storage.rocks_db_storage import save_variants


HOME = os.path.expanduser("~")
ROOT = os.path.join(HOME, ".app_storage")
BASE_DIR = os.path.join(ROOT, "base")
P1_DIR = os.path.join(ROOT, "P1")


def get_generator_by_type(type: GenType, prefix: str):
    if type == GenType.BASE:
        return NotebookGenerator(prefix=prefix)
    elif type == GenType.PRACTICE_1:
        return Practice_1(prefix=prefix)
    elif type == GenType.PRACTICE_2:
        return Practice_2(prefix=prefix)
    elif type == GenType.PRACTICE_3:
        return Practice_3(prefix=prefix)


async def generate_for_group(
    lab: Lab, group: Group, students: List[Student]
) -> List[Variant]:
    """
    Generates variants for group by lab and store it in local directory

    Args:
        lab: Lab for generate
        group: Group for generate.

    Returns:
        The paths to variants.
    """

    prefix = f"L{lab.id}_GR{group.id}"

    generator = get_generator_by_type(type=lab.generator_type, prefix=prefix)

    variants = await generator.generate_notebooks(n=len(students))

    store_vars = await save_variants(variants=variants)

    return store_vars
