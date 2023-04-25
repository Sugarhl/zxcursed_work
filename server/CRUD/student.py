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


async def get_student_by_id(db: AsyncSession, user_id: int):
    stmt = select(Student).where(Student.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
