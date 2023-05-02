from typing import List, Optional
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from server.models.lab_variant import LabVariant


async def create_lab_variant_from_dict(
    db: AsyncSession, lab_variant: dict
) -> LabVariant:
    lab_variant_obj = LabVariant(**lab_variant)
    db.add(lab_variant_obj)
    await db.commit()
    await db.refresh(lab_variant_obj)
    return lab_variant_obj


async def get_lab_variant(
    db: AsyncSession, lab_variant_id: int
) -> Optional[LabVariant]:
    return await db.get(LabVariant, lab_variant_id)


async def get_all_lab_variants(db: AsyncSession) -> List[LabVariant]:
    result = await db.execute(select(LabVariant))
    return result.scalars().all()


async def get_all_lab_variants_by_lab_id(
    db: AsyncSession, lab_id: int
) -> List[LabVariant]:
    result = await db.execute(select(LabVariant).filter(LabVariant.lab_id == lab_id))
    return result.scalars().all()


async def delete_lab_variant(
    db: AsyncSession, lab_variant_id: int
) -> Optional[LabVariant]:
    lab_variant = await get_lab_variant(db, lab_variant_id)
    if lab_variant:
        db.delete(lab_variant)
        await db.commit()
    else:
        return lab_variant
