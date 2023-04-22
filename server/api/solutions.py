from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

import server.schemas as schemas
from server.crud import create_comment, create_solution
from server.database import get_db
from server.token import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
bearer = HTTPBearer()


@router.post("/upload_solution", status_code=status.HTTP_201_CREATED)
async def upload_solution(solution: schemas.SolutionUpload, auth: HTTPAuthorizationCredentials = Depends(bearer), db: AsyncSession = Depends(get_db)):
    try:
        user_id, user_type = decode_access_token(auth.credentials)
        print('AUTHORIZED')

        if user_type != "Student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students are allowed to upload solutions"
            )

        solution_id = await create_solution(db, user_id, solution.lab_variant_id, solution.solution_file)
        return {"solution_id": solution_id}

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())


@router.post("/create_lab_solution_comment", status_code=status.HTTP_201_CREATED)
async def create_lab_solution_comment(comment: schemas.LabSolutionCommentCreate, auth: HTTPAuthorizationCredentials = Depends(bearer), db: AsyncSession = Depends(get_db)):
    try:
        user_id, user_type = decode_access_token(auth.credentials)

        comment_id = await create_comment(db=db,
                                          comment=comment,
                                          user_id=user_id,
                                          user_type=user_type)
        return {"comment_id": comment_id}

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())
