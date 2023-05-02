import os
from typing import List


from server.generation.base import GenType, NotebookGenerator, Variant
from server.models.lab import Lab
from server.models.group import Group
from server.models.student import Student


HOME = os.path.expanduser("~")
ROOT = os.path.join(HOME, ".app_storage")
BASE_DIR = os.path.join(ROOT, "base")


def get_generator_by_type(type: GenType, prefix: str):
    if type == GenType.BASE:
        return NotebookGenerator(prefix=prefix, directory=BASE_DIR + prefix)

    elif type == GenType.NOT_BASE:
        return NotebookGenerator(prefix=prefix, directory=BASE_DIR + prefix)


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

    return variants
