import datetime
from typing import Optional
import bcrypt
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import server.models as models
import server.schemas as schemas


# Some utils
def generate_salt() -> str:
    return bcrypt.gensalt().decode("utf-8")


async def add_to_db(obj, db: AsyncSession, ) -> int:
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj.id


# Create statements
async def create_user(db: AsyncSession,
                      user_in: schemas.UserIn,
                      user_type: str,
                      user_id: int) -> int:
    salt = generate_salt()
    hashed_password = bcrypt.hashpw(
        user_in.password.encode("utf-8"), salt.encode("utf-8"))

    user = models.User(user_id=user_id,
                       user_type=user_type,
                       username=user_in.username,
                       password=hashed_password.decode("utf-8"),
                       salt=salt)

    return await add_to_db(user, db=db)


async def create_student(db: AsyncSession, student: schemas.UserIn) -> int:
    db_student = models.Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
    )
    return await add_to_db(db_student, db=db)


async def create_tutor(db: AsyncSession, tutor: schemas.UserIn) -> int:
    db_tutor = models.Tutor(
        first_name=tutor.first_name,
        last_name=tutor.last_name,
        email=tutor.email,
    )
    return await add_to_db(db_tutor, db=db)


async def create_solution(db: AsyncSession,
                          student_id: int,
                          lab_variant_id: int,
                          solution_file: Optional[UploadFile]) -> int:
    solution_filename = None
    file_data = None
    if solution_file:
        solution_filename = solution_file.filename
        file_data = await solution_file.read()

    solution = models.LabSolution(
        student_id=student_id,
        lab_variant_id=lab_variant_id,
        solution_filename=solution_filename,
        file_data=file_data)
    return await add_to_db(solution, db=db)


async def create_comment(db: AsyncSession,
                         comment: schemas.LabSolutionCommentCreate,
                         user_id: int,
                         user_type: int) -> int:
    db_comment = models.LabSolutionComment(
        solution_id=comment.solution_id,
        user_id=user_id,
        user_type=user_type,
        reply_id=comment.reply_id,
        comment_text=comment.text,
        created_date=datetime.datetime.utcnow(),
        updated_date=datetime.datetime.utcnow())
    print('ready to add')
    return await add_to_db(db_comment, db=db)


# Get statements
async def get_user_by_username(db: AsyncSession, username: str):
    stmt = select(models.User).where(models.User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int):
    stmt = select(models.User).where(models.User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def verify_password(password: str, salt: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")) and bcrypt.checkpw(salt.encode("utf-8"), hashed_password.encode("utf-8"))
