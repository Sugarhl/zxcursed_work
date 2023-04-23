from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import server.schemas as schemas
from server.models.student import Student
from server.CRUD.utils import add_to_db


async def create_student(db: AsyncSession, student: schemas.UserIn) -> int:
    db_student = Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
    )
    return await add_to_db(db_student, db=db)
