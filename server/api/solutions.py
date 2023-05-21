from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from server.CRUD.lab_variant import get_lab_variant_checked, update_lab_variant


import server.schemas as schemas
from server.CRUD.solution import (
    create_lab_solution,
    get_lab_solution_checked,
    update_lab_solution,
)

from server.database import get_db
from server.storage.rocks_db_storage import RocksDBStorage
from server.token import auth_by_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from server.utils import UserType

from server.validation.checks import (
    file_ext_check,
    lab_var_check_access,
    student_access_check,
    tutor_access_check,
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
bearer = HTTPBearer()


@router.post(
    "/upload_solution",
    response_model=schemas.LabSolution,
    status_code=status.HTTP_201_CREATED,
)
async def upload_solution(
    lab_variant_id: int = Form(...),
    comment: Optional[str] = None,
    file: UploadFile = File(..., format=[".ipynb"]),
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    try:
        student, user_type = await auth_by_token(db=db, auth=auth)
        student_access_check(user_type)

        variant = await get_lab_variant_checked(db, lab_variant_id)
        lab_var_check_access(variant, student)

        file_ext_check(file)
        file_content = await file.read()
        storage = RocksDBStorage()
        file_key = await storage.save_file(file_content)

        solution_db = await create_lab_solution(
            db=db,
            lab_variant_id=lab_variant_id,
            solution_filename=file.filename,
            file_key=file_key,
            student_comment=comment,
        )

        return solution_db

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())


@router.get("/get", status_code=status.HTTP_200_OK, response_model=schemas.LabSolution)
async def get_solution(
    solution_id: int,
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    try:
        student, user_type = await auth_by_token(db=db, auth=auth)

        lab_solution = await get_lab_solution_checked(
            db=db, lab_solution_id=solution_id
        )

        if user_type == UserType.STUDENT:
            variant = await get_lab_variant_checked(db, lab_solution.lab_variant_id)
            lab_var_check_access(variant, student)

        return lab_solution

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())


@router.post(
    "/mark", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.LabSolution
)
async def mark_solution(
    solution_mark: schemas.LabSolutionMark,
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    try:
        tutor, user_type = await auth_by_token(db=db, auth=auth)
        tutor_access_check(user_type)

        solution_diff = {
            "tutor_comment": solution_mark.comment,
            "tutor_mark": solution_mark.mark,
        }

        lab_solution = await update_lab_solution(
            db=db,
            id=solution_mark.solution_id,
            diff_data=solution_diff,
        )

        await update_lab_variant(
            db=db, id=lab_solution.id, diff_data={"tutor_for_check_id": tutor.id}
        )

        return lab_solution

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())
