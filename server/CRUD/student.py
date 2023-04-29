from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import server.schemas as schemas
from server.models.student import Student
from server.CRUD.utils import add_to_db
from server.validation.checks import student_check


async def create_student(db: AsyncSession, student: schemas.UserIn) -> int:
    db_student = Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
    )
    return await add_to_db(db_student, db=db)


async def get_students_by_group(db: AsyncSession, group_id: int) -> List[Student]:
    stmt = select(Student).where(Student.group_id == group_id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_student_by_id(db: AsyncSession, user_id: int):
    stmt = select(Student).where(Student.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_student_checked(db: AsyncSession, id: int):
    student = await db.get(Student, id)
    student_check(student)
    return student
