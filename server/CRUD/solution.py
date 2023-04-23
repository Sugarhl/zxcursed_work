from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import server.schemas as schemas
from server.models.lab_solution import LabSolution
from server.CRUD.utils import add_to_db


async def create_solution(db: AsyncSession,
                          student_id: int,
                          lab_variant_id: int,
                          solution_file: UploadFile) -> int:
    solution_filename = solution_file.filename
    file_data = await solution_file.read()

    solution = LabSolution(
        student_id=student_id,
        lab_variant_id=lab_variant_id,
        solution_filename=solution_filename,
        file_data=file_data)
    return await add_to_db(solution, db=db)
