
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

import server.schemas as schemas
from server.CRUD.lab import create_lab, get_all_labs, get_all_labs_by_tutor_id
from server.database import get_db
from server.token import auth_by_token
from server.utils import UserType

router = APIRouter()
bearer = HTTPBearer()


@router.post("/variants", status_code=status.HTTP_201_CREATED)
async def genrate_for_group(lab: schemas.LabCreate, auth: HTTPAuthorizationCredentials = Depends(bearer), db: AsyncSession = Depends(get_db)):
    tutor, user_type = await auth_by_token(db=db, token=auth.credentials)

    if user_type != UserType.TUTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only tutors are allowed to create labs"
        )
