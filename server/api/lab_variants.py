from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession


import server.schemas as schemas

from server.CRUD.group import get_group_checked
from server.CRUD.lab import get_lab_checked
from server.CRUD.lab_variant import (
    create_lab_variant_from_dict,
    get_all_lab_variants_by_student_id,
    get_lab_variant,
    get_lab_variant_checked,
)
from server.CRUD.student import get_student_checked, get_students_by_group

from server.generation.base import Variant
from server.generation.generate import generate_for_group

from server.models.lab import Lab
from server.models.lab_variant import LabVariant
from server.models.student import Student

from server.database import get_db
from server.token import auth_by_token
from server.validation.checks import student_access_check, tutor_access_check

router = APIRouter()
bearer = HTTPBearer(auto_error=False)


async def assign_variants(
    lab: Lab, variants: List[Variant], students: List[Student], db: AsyncSession
) -> List[LabVariant]:
    assert len(variants) == len(students)
    lab_vars = []

    for i, variant in enumerate(variants):
        lab_variant_data = {
            "lab_id": lab.id,
            "student_id": students[i].id,
            "variant_number": i,
            "variant_filename": variant.file_name,
            "file_key": variant.key,
        }

        lab_variant = await create_lab_variant_from_dict(db, lab_variant_data)
        lab_vars.append(lab_variant)

    return lab_vars


@router.post(
    "/generate",
    status_code=status.HTTP_201_CREATED,
    response_model=List[schemas.LabVariant],
)
async def genrate_for_group_route(
    params: schemas.GenerateVariantsParams,
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    _, user_type = await auth_by_token(db=db, auth=auth)

    tutor_access_check(user_type)

    lab = await get_lab_checked(db, params.lab_id)

    group = await get_group_checked(db, params.group_id)

    students = await get_students_by_group(db, params.group_id)
    if len(students) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty group",
        )

    variants = await generate_for_group(lab=lab, group=group, students=students)

    lab_variants = await assign_variants(
        lab=lab, variants=variants, students=students, db=db
    )

    return lab_variants


@router.post(
    "/student/all",
    status_code=status.HTTP_201_CREATED,
    response_model=List[schemas.LabVariant],
)
async def get_student_vars(
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    student, user_type = await auth_by_token(db=db, auth=auth)

    student_access_check(user_type)

    lab_variants = await get_all_lab_variants_by_student_id(
        db=db, student_id=student.id
    )

    return lab_variants


@router.post(
    "/student/{lab_var_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.LabVariant,
)
async def get_student_var_by_id(
    lab_var_id: int,
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    student, user_type = await auth_by_token(db=db, auth=auth)
    student_access_check(user_type)

    lab_variant = await get_lab_variant(db=db, lab_variant_id=lab_var_id)

    if lab_variant.student_id != student.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have acess to lab variant",
        )

    return lab_variant


@router.post(
    "/tutor/all-by-student/{student_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=List[schemas.LabVariant],
)
async def get_varinats_by_student_id(
    student_id: int,
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    _, user_type = await auth_by_token(db=db, auth=auth)

    tutor_access_check(user_type)

    student = await get_student_checked(db, student_id)

    lab_variants = await get_all_lab_variants_by_student_id(
        db=db, student_id=student.id
    )

    return lab_variants


@router.post(
    "/tutor/variant/{lab_var_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.LabVariant,
)
async def get_var_by_id(
    lab_var_id: int,
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    tutor, user_type = await auth_by_token(db=db, auth=auth)
    tutor_access_check(user_type)

    lab_variant = await get_lab_variant_checked(db=db, lab_variant_id=lab_var_id)

    return lab_variant
