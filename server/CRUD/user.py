import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from server.models.student import Student
from server.models.tutor import Tutor
from server.models.user import User

import server.schemas as schemas
from server.utils import UserType, generate_salt, generate_salted_password
from server.CRUD.utils import add_to_db

# Create statements


async def create_user(
    db: AsyncSession, user_in: schemas.UserIn, user_type: UserType, user_id: int
) -> int:
    salt = generate_salt()
    hashed_password = generate_salted_password(salt=salt, password=user_in.password)

    user = User(
        user_id=user_id,
        user_type=user_type,
        username=user_in.username,
        password=hashed_password,
        salt=salt,
    )

    return await add_to_db(user, db=db)


# Get statements
async def get_user_by_username(db: AsyncSession, username: str):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str, user_type: UserType):
    if user_type == UserType.STUDENT:
        stmt = select(Student).where(Student.email == email)
    elif user_type == UserType.TUTOR:
        stmt = select(Tutor).where(Tutor.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
