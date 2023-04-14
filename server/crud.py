import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import server.models as models
import server.schemas as schemas


def generate_salt() -> str:
    return bcrypt.gensalt().decode("utf-8")


async def create_user(db: AsyncSession, user_in: schemas.UserIn, user_type: str, user_id: int) -> int:
    salt = generate_salt()
    hashed_password = bcrypt.hashpw(
        user_in.password.encode("utf-8"), salt.encode("utf-8"))

    user = models.User(user_id=user_id,
                       user_type=user_type,
                       username=user_in.username,
                       password=hashed_password.decode("utf-8"))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user.id


async def create_student(db: AsyncSession, student: schemas.UserIn) -> int:
    db_student = models.Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
    )
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student.id


async def create_tutor(db: AsyncSession, tutor: schemas.UserIn) -> int:
    db_tutor = models.Tutor(
        first_name=tutor.first_name,
        last_name=tutor.last_name,
        email=tutor.email,
    )
    db.add(db_tutor)
    await db.commit()
    await db.refresh(db_tutor)
    return db_tutor.id


async def get_user_by_username(db: AsyncSession, username: str):
    stmt = select(models.User).where(models.User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user(db: AsyncSession, user_id: int, user_type: str):
    if user_type == "Student":
        stmt = select(models.Student).where(models.Student.id == user_id)
    elif user_type == "Tutor":
        stmt = select(models.Tutor).where(models.Tutor.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# Add more CRUD operations for other models (Lab, LabVariant, LabSolution, LabResult) as needed.
