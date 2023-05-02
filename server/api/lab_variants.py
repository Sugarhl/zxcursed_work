from typing import List
from uuid import uuid4
from server.CRUD.group import get_group_checked
from server.CRUD.lab import get_lab_checked
from server.CRUD.lab_variant import create_lab_variant_from_dict
from server.CRUD.student import get_students_by_group
from server.generation.base import Variant
from server.generation.generate import generate_for_group
from server.models.lab import Lab
from server.models.lab_variant import LabVariant
from server.models.student import Student
import server.schemas as schemas

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.ext.asyncio import AsyncSession

from server.database import get_db
from server.token import auth_by_token
from server.validation.checks import tutor_access_check

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
