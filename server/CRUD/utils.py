from sqlalchemy.ext.asyncio import AsyncSession


async def add_to_db(obj, db: AsyncSession) -> int:
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj.id