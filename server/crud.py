from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import server.models as models
import server.schemas as schemas


async def create_user(db: AsyncSession, user: models.User):
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def create_student(db: AsyncSession, student: schemas.UserIn):
    db_student = models.Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
    )
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student


async def create_tutor(db: AsyncSession, tutor: schemas.UserIn):
    db_tutor = models.Tutor(
        first_name=tutor.first_name,
        last_name=tutor.last_name,
        email=tutor.email,
    )
    db.add(db_tutor)
    await db.commit()
    await db.refresh(db_tutor)
    return db_tutor


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
