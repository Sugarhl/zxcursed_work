from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import server.schemas as schemas
from server.models.tutor import Tutor
from server.CRUD.utils import add_to_db
from server.validation.checks import tutor_check


async def create_tutor(db: AsyncSession, tutor: schemas.UserIn) -> int:
    db_tutor = Tutor(
        first_name=tutor.first_name,
        last_name=tutor.last_name,
        email=tutor.email,
    )
    return await add_to_db(db_tutor, db=db)


async def get_tutor_by_id(db: AsyncSession, user_id: int):
    stmt = select(Tutor).where(Tutor.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_tutor_checked(db: AsyncSession, id: int):
    tutor = await db.get(Tutor, id)
    tutor_check(tutor)
    return tutor
