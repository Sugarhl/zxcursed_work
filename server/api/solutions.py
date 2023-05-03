from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from server.CRUD.lab_variant import get_lab_variant


import server.schemas as schemas
from server.CRUD.solution import create_lab_solution

from server.database import get_db
from server.storage.rocks_db_storage import RocksDBStorage
from server.token import auth_by_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from server.validation.checks import lab_var_check_access, student_access_check

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
bearer = HTTPBearer()


@router.post(
    "/upload_solution",
    response_model=schemas.LabSolution,
    status_code=status.HTTP_201_CREATED,
)
async def upload_solution(
    solution: schemas.SolutionUpload,
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    try:
        student, user_type = auth_by_token(auth)

        student_access_check(user_type)

        variant = await get_lab_variant(db, solution.lab_variant_id)

        lab_var_check_access(variant, student)
        storage = RocksDBStorage()

        file_key = storage.save_file(solution.solution_file.file)

        solution_db = await create_lab_solution(
            db=db,
            lab_variant_id=solution.lab_variant_id,
            solution_filename=solution.solution_file.filename,
            file_key=file_key,
            student_comment=solution.comment,
        )

        return schemas.LabSolution(
            id=solution.id,
            lab_variant_id=solution_db.lab_variant_id,
            filename=solution_db.solution_filename,
            file_key=solution_db.file_key,
        )

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())
