from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

import server.schemas as schemas
from server.CRUD.lab import create_lab, get_all_labs_by_tutor_id
from server.database import get_db
from server.token import auth_by_token
from server.utils import UserType

router = APIRouter()
bearer = HTTPBearer()


@router.post("/create_lab", status_code=status.HTTP_201_CREATED)
async def create_lab(lab: schemas.LabCreate, auth: HTTPAuthorizationCredentials = Depends(bearer), db: AsyncSession = Depends(get_db)):
    try:
        tutor = await auth_by_token(db=db, token=auth.credentials)

        if tutor.user_type != UserType.TUTOR:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only tutors are allowed to create labs"
            )

        lab_id = await create_lab(db=db, lab=lab, tutor_id=tutor.user_id)
        return {"lab_id": lab_id}

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())


@router.get("/labs", response_model=list[schemas.LabOut])
async def get_all_labs(auth: HTTPAuthorizationCredentials = Depends(bearer), db: AsyncSession = Depends(get_db)):
    try:
        tutor = await auth_by_token(db=db, token=auth.credentials)

        if tutor.user_type == UserType.TUTOR:
            labs = await get_all_labs_by_tutor_id(db, tutor.user_id)
        else:
            labs = await get_all_labs(db)

        return labs

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())
