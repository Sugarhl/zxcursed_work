from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from server.models.lab import Lab
from server.schemas import LabCreate
from server.CRUD.utils import add_to_db
from server.validation.checks import lab_check


async def create_lab(db: AsyncSession, lab: LabCreate, tutor_id: int) -> Lab:
    lab_obj = Lab(
        lab_name=lab.lab_name,
        description=lab.description,
        date_start=lab.date_start,
        deadline=lab.deadline,
        tutor_id=tutor_id,
        generator_type=lab.generator_type,
    )
    return await add_to_db(db=db, obj=lab_obj)


async def get_lab(db: AsyncSession, lab_id: int) -> Optional[Lab]:
    return await db.get(Lab, lab_id)


async def get_lab_checked(db: AsyncSession, lab_id: int) -> Lab:
    lab = await get_lab(db=db, lab_id=lab_id)
    lab_check(lab)
    return lab


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
