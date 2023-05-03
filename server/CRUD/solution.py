import select
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.lab_solution import LabSolution
from server.validation.checks import solution_check


async def create_lab_solution(
    db: AsyncSession,
    lab_variant_id: int,
    solution_filename: str,
    file_key: str,
    student_comment: Optional[str],
) -> LabSolution:
    lab_solution = LabSolution(
        lab_variant_id=lab_variant_id,
        solution_filename=solution_filename,
        file_key=file_key,
        student_comment=student_comment,
    )
    db.add(lab_solution)
    await db.commit()
    await db.refresh(lab_solution)
    return lab_solution


async def get_lab_solution(db: AsyncSession, lab_solution_id: int) -> LabSolution:
    return await db.get(LabSolution, lab_solution_id)


async def get_lab_solution_checked(
    db: AsyncSession, lab_solution_id: int
) -> LabSolution:
    solution = await db.get(LabSolution, lab_solution_id)
    solution_check(solution)
    return solution


async def get_lab_solutions_by_lab_variant_id(
    db: AsyncSession, lab_variant_id: int
) -> list[LabSolution]:
    result = await db.execute(
        select(LabSolution).where(LabSolution.lab_variant_id == lab_variant_id)
    )
    return result.scalars().all()


async def get_lab_solutions_by_lab_variant_id_checked(
    db: AsyncSession, lab_variant_id: int
) -> list[LabSolution]:
    solution = get_lab_solutions_by_lab_variant_id(db, lab_variant_id)
    solution_check(solution)
    return solution


async def update_lab_solution(
    db: AsyncSession, lab_solution_id: int, lab_solution_data: dict
) -> LabSolution:
    lab_solution = await get_lab_solution(db, lab_solution_id)
    for key, value in lab_solution_data.items():
        setattr(lab_solution, key, value)
    await db.commit()
    await db.refresh(lab_solution)
    return lab_solution


async def delete_lab_solution(db: AsyncSession, lab_solution_id: int) -> None:
    lab_solution = await get_lab_solution(db, lab_solution_id)
    db.delete(lab_solution)
    await db.commit()
