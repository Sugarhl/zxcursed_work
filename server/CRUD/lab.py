from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from server.models.lab import Lab
from server.schemas import LabCreate
from server.CRUD.utils import add_to_db


async def create_lab(db: AsyncSession, lab: LabCreate, tutor_id: int) -> int:
    lab_obj = Lab(
        lab_name=lab.lab_name,
        description=lab.description,
        date_start=lab.date_start,
        deadline=lab.deadline,
        tutor_id=tutor_id,
        generator_type=lab.generator_type,
    )
    return await add_to_db(db=db, obj=lab_obj)


async def get_lab(db: AsyncSession, lab_id: int) -> Lab:
    return await db.get(Lab, lab_id)


async def get_all_labs_by_tutor_id(db: AsyncSession, tutor_id: int) -> list[Lab]:
    labs = await db.execute(select(Lab).filter(Lab.tutor_id == tutor_id))
    return labs.scalars().all()


async def get_all_labs(db: AsyncSession) -> list[Lab]:
    labs = await db.execute(select(Lab))
    return labs.scalars().all()


async def delete_lab(db: AsyncSession, lab_id: int):
    lab_obj = await get_lab(db, lab_id)
    db.delete(lab_obj)
    await db.commit()
