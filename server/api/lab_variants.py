from server.CRUD.group import get_group_checked
from server.CRUD.lab import get_lab_checked
from server.CRUD.student import get_students_by_group
from server.generation.generate import generate_for_group
import server.schemas as schemas

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.ext.asyncio import AsyncSession

from server.database import get_db
from server.token import auth_by_token
from server.validation.checks import tutor_access_check

router = APIRouter()
bearer = HTTPBearer()


@router.post(
    "/variants",
    status_code=status.HTTP_201_CREATED,
    response_model=list[str],
)
async def genrate_for_group_route(
    params: schemas.GenerateVariantsParams,
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    _, user_type = await auth_by_token(db=db, token=auth.credentials)

    tutor_access_check(user_type)

    lab = await get_lab_checked(db, params.lab_id)

    group = await get_group_checked(db, params.group_id)
    students = await get_students_by_group(db, params.group_id)

    variant_paths = generate_for_group(lab=lab, group=group, students=students)

    return variant_paths
