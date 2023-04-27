from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

import server.schemas as schemas
from server.CRUD.lab import create_lab, get_all_labs, get_all_labs_by_tutor_id
from server.database import get_db
from server.token import auth_by_token
from server.utils import UserType, tutor_check

router = APIRouter()
bearer = HTTPBearer()


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_lab_route(lab: schemas.LabCreate, auth: HTTPAuthorizationCredentials = Depends(bearer), db: AsyncSession = Depends(get_db)):
    try:
        tutor, user_type = await auth_by_token(db=db, token=auth.credentials)

        tutor_check(user_type)

        lab_id = await create_lab(db=db, lab=lab, tutor_id=tutor.id)
        return {"lab_id": lab_id}

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())


@router.get("/tutor/all", response_model=list[schemas.LabOut])
async def get_all_labs_route(auth: HTTPAuthorizationCredentials = Depends(bearer), db: AsyncSession = Depends(get_db)):
    try:
        tutor, user_type = await auth_by_token(db=db, token=auth.credentials)
        tutor_check(user_type)
        labs = await get_all_labs_by_tutor_id(db, tutor.id)

        return labs

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())


@router.get("/all", response_model=list[schemas.LabOut])
async def get_all_labs_route(auth: HTTPAuthorizationCredentials = Depends(bearer), db: AsyncSession = Depends(get_db)):
    try:
        await auth_by_token(db=db, token=auth.credentials)

        labs = await get_all_labs(db)

        return labs

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())
