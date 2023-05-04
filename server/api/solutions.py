from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from server.CRUD.lab_variant import get_lab_variant_checked


import server.schemas as schemas
from server.CRUD.solution import create_lab_solution

from server.database import get_db
from server.storage.rocks_db_storage import RocksDBStorage
from server.token import auth_by_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from server.validation.checks import (
    file_ext_check,
    lab_var_check_access,
    student_access_check,
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

        return schemas.LabSolution(
            id=solution_db.id,
            lab_variant_id=solution_db.lab_variant_id,
            filename=solution_db.solution_filename,
            file_key=solution_db.file_key,
        )

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())
