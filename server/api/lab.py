from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from server.CRUD.group import get_group_checked
from server.CRUD.lab_variant import get_all_lab_variants_by_student_id
from server.generation.generators.base import GenType

import server.schemas as schemas
from server.CRUD.lab import (
    create_lab,
    get_all_labs,
    get_all_labs_by_tutor_id,
    get_labs_checked,
)
from server.database import get_db
from server.token import auth_by_token
from server.validation.checks import student_access_check, tutor_access_check

router = APIRouter()
bearer = HTTPBearer()


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_lab_route(
    lab: schemas.LabCreate,
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    try:
        tutor, user_type = await auth_by_token(db=db, auth=auth)

        tutor_access_check(user_type)

        await get_group_checked(db, lab.group_id)

        lab = await create_lab(db=db, lab=lab, tutor_id=tutor.id)
        return {"lab_id": lab.id}

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())


@router.get("/get/tutor/all", response_model=list[schemas.LabOut])
async def get_all_tutor_labs_route(
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    try:
        tutor, user_type = await auth_by_token(db=db, auth=auth)
        tutor_access_check(user_type)
        labs = await get_all_labs_by_tutor_id(db, tutor.id)

        return labs

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())


@router.get("/get/student/all", response_model=list[schemas.LabOut])
async def get_all_student_labs_route(
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    try:
        student, user_type = await auth_by_token(db=db, auth=auth)
        student_access_check(user_type)
        lab_variants = await get_all_lab_variants_by_student_id(db, student.id)
        lab_ids = list(map(lambda x: x.lab_id, lab_variants))
        labs = await get_labs_checked(db=db, lab_ids=lab_ids)
        return labs

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())


@router.get("/get/all", response_model=list[schemas.LabOut])
async def get_all_labs_route(
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    try:
        await auth_by_token(db=db, auth=auth)

        labs = await get_all_labs(db)

        return labs

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())


@router.get("/get/generators")
async def get_generators():
    return {"generators": [generator.value for generator in GenType]}
