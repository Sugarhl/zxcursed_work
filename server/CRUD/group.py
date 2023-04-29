from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from server.models.group import Group
from server.schemas import GroupCreate, GroupUpdate
from server.validation.checks import group_check


async def create_group(db: AsyncSession, group: GroupCreate, tutor_id: int) -> int:
    group_obj = Group(name=group.name, tutor_id=tutor_id)
    db.add(group_obj)
    await db.commit()
    await db.refresh(group_obj)
    return group_obj.id


async def get_group(db: AsyncSession, group_id: int) -> Group:
    return await db.get(Group, group_id)


async def get_group_checked(db: AsyncSession, group_id: int) -> Group:
    group = await get_group(db, group_id)
    group_check(group)
    return group


async def get_all_groups_by_tutor_id(db: AsyncSession, tutor_id: int) -> list[Group]:
    groups = await db.execute(select(Group).filter(Group.tutor_id == tutor_id))
    return groups.scalars().all()


async def get_all_groups(db: AsyncSession) -> list[Group]:
    groups = await db.execute(select(Group))
    return groups.scalars().all()


async def update_group(db: AsyncSession, group_id: int, group: GroupUpdate):
    group_obj = await get_group(db, group_id)
    for field, value in group.dict(exclude_unset=True).items():
        setattr(group_obj, field, value)
    await db.commit()


async def delete_group(db: AsyncSession, group_id: int):
    group_obj = await get_group(db, group_id)
    db.delete(group_obj)
    await db.commit()
