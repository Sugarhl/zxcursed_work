from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from server.CRUD.student import get_student_by_id

import server.schemas as schemas
from server.CRUD.group import create_group, get_all_groups, get_all_groups_by_tutor_id, get_group, update_group
from server.database import get_db
from server.token import auth_by_token
from server.utils import UserType, tutor_check

router = APIRouter()
bearer = HTTPBearer()


def group_check(group):
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Group does not exist")


def group_check_access(group, tutor):
    if group.tutor_id != tutor.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this group"
        )


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_group_route(group: schemas.GroupCreate, auth: HTTPAuthorizationCredentials = Depends(bearer), db: AsyncSession = Depends(get_db)):
    try:
        tutor, user_type = await auth_by_token(db=db, token=auth.credentials)
        tutor_check(user_type=user_type)

        group_id = await create_group(db=db, group=group, tutor_id=tutor.id)
        return {"group_id": group_id}

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())


@router.get("/all", response_model=list[schemas.GroupOut])
async def get_all_groups_route(auth: HTTPAuthorizationCredentials = Depends(bearer), db: AsyncSession = Depends(get_db)):
    try:
        tutor, user_type = await auth_by_token(db=db, token=auth.credentials)

        tutor_check(user_type=user_type)
        groups = await get_all_groups(db)

        return groups

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())


@router.get("/tutor/all", response_model=list[schemas.GroupOut])
async def get_all_groups_route(auth: HTTPAuthorizationCredentials = Depends(bearer), db: AsyncSession = Depends(get_db)):
    try:
        tutor, user_type = await auth_by_token(db=db, token=auth.credentials)
        tutor_check(user_type=user_type)

        groups = await get_all_groups_by_tutor_id(db, tutor.id)

        return groups

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())


@router.get("/get/{group_id}", response_model=schemas.GroupOut)
async def get_group_route(group_id: int, auth: HTTPAuthorizationCredentials = Depends(bearer), db: AsyncSession = Depends(get_db)):
    try:
        _, _ = await auth_by_token(db=db, token=auth.credentials)
        group = await get_group(db, group_id)
        group_check(group)
        return group

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())


@router.put("/update/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_group_route(group_id: int, group: schemas.GroupUpdate, auth: HTTPAuthorizationCredentials = Depends(bearer), db: AsyncSession = Depends(get_db)):
    try:
        tutor, user_type = await auth_by_token(db=db, token=auth.credentials)
        tutor_check(user_type=user_type)

        existing_group = await get_group(db, group_id)

        group_check(existing_group)

        group_check_access(existing_group, tutor)

        await update_group(db, group_id, group)

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())


@router.put("/set_student", status_code=status.HTTP_204_NO_CONTENT)
async def set_student_group_route(params: schemas.SetStudentToGroup, auth: HTTPAuthorizationCredentials = Depends(bearer), db: AsyncSession = Depends(get_db)):
    try:
        user, user_type = await auth_by_token(db=db, token=auth.credentials)

        group = await get_group(db, params.group_id)
        group_check(group)

        student = await get_student_by_id(db, params.student_id)

        if not student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Student does not exist")

        if user_type == UserType.STUDENT:
            if student.id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only student and tutor can change his group"
                )

        student.group_id = group.id
        await db.commit()

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())
