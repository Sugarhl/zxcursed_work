from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from server.CRUD.student import get_student_checked

import server.schemas as schemas
from server.CRUD.group import (
    create_group,
    get_all_groups,
    get_all_groups_by_tutor_id,
    get_group_checked,
    update_group,
)
from server.database import get_db
from server.token import auth_by_token
from server.validation.checks import (
    UserType,
    group_check_access,
    tutor_access_check,
)

router = APIRouter()
bearer = HTTPBearer()


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_group_route(
    group: schemas.GroupCreate,
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    try:
        tutor, user_type = await auth_by_token(db=db, auth=auth)
        tutor_access_check(user_type=user_type)

        group_id = await create_group(db=db, group=group, tutor_id=tutor.id)
        return {"group_id": group_id}

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.errors(),
        )


@router.get("/all", response_model=list[schemas.GroupOut])
async def get_all_groups_route(
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    try:
        _, user_type = await auth_by_token(db=db, auth=auth)

        tutor_access_check(user_type=user_type)
        groups = await get_all_groups(db)

        return groups

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.errors(),
        )


@router.get("/tutor/all", response_model=list[schemas.GroupOut])
async def get_all_tutor_groups_route(
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    try:
        tutor, user_type = await auth_by_token(db=db, auth=auth)
        tutor_access_check(user_type=user_type)

        groups = await get_all_groups_by_tutor_id(db, tutor.id)

        return groups

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.errors(),
        )


@router.get("/get/{group_id}", response_model=schemas.GroupOut)
async def get_group_route(
    group_id: int,
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    try:
        _, _ = await auth_by_token(db=db, auth=auth)
        return await get_group_checked(db, group_id)

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.errors(),
        )


@router.put("/update/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_group_route(
    group_id: int,
    group: schemas.GroupUpdate,
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    try:
        tutor, user_type = await auth_by_token(db=db, auth=auth)
        tutor_access_check(user_type=user_type)

        existing_group = await get_group_checked(db, group_id)

        group_check_access(existing_group, tutor)

        await update_group(db, group_id, group)

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())


@router.put("/set_student", status_code=status.HTTP_200_OK)
async def set_student_group_route(
    params: schemas.SetStudentToGroup,
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    try:
        user, user_type = await auth_by_token(db=db, auth=auth)

        group = await get_group_checked(db, params.group_id)

        student = await get_student_checked(db, params.student_id)

        if user_type == UserType.STUDENT:
            if student.id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only student and tutor can change his group",
                )

        student.group_id = group.id
        await db.commit()

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())
