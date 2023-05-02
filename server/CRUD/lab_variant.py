from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from server.models.lab_variant import LabVariant


async def create_lab_variant(db: AsyncSession, lab_variant: dict) -> LabVariant:
    lab_variant_obj = LabVariant(**lab_variant)
    db.add(lab_variant_obj)
    await db.commit()
    await db.refresh(lab_variant_obj)
    return lab_variant_obj


async def get_lab_variant(db: AsyncSession, lab_variant_id: int) -> LabVariant:
    stmt = select(LabVariant).filter(LabVariant.id == lab_variant_id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def get_lab_variants_by_student_id(
    db: AsyncSession, student_id: int
) -> list[LabVariant]:
    stmt = select(LabVariant).filter(LabVariant.student_id == student_id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_all_lab_variants(db: AsyncSession) -> list[LabVariant]:
    stmt = select(LabVariant)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_all_lab_variants_by_lab_id(
    db: AsyncSession, lab_id: int
) -> list[LabVariant]:
    stmt = select(LabVariant).filter(LabVariant.lab_id == lab_id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def update_lab_variant(
    db: AsyncSession, lab_variant_id: int, lab_variant_data: dict
) -> LabVariant:
    stmt = (
        LabVariant.__table__.update()
        .where(LabVariant.id == lab_variant_id)
        .values(**lab_variant_data)
        .returning(LabVariant)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalars().first()


async def delete_lab_variant(db: AsyncSession, lab_variant_id: int) -> LabVariant:
    lab_variant = await get_lab_variant(db, lab_variant_id)
    db.delete(lab_variant)
    await db.commit()
    return lab_variant
