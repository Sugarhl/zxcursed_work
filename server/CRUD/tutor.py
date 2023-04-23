from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import server.schemas as schemas
from server.models.tutor import Tutor
from server.CRUD.utils import add_to_db


async def create_tutor(db: AsyncSession, tutor: schemas.UserIn) -> int:
    db_tutor = Tutor(
        first_name=tutor.first_name,
        last_name=tutor.last_name,
        email=tutor.email,
    )
    return await add_to_db(db_tutor, db=db)
