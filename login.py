from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
import bcrypt

from schemas import UserIn
from database import async_engine
from crud import get_user_by_username

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

async def async_session_manager():
    async with async_session() as s:
        yield s

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(async_session)):
    user_in = UserIn(username=form_data.username, password=form_data.password)
    user = await get_user_by_username(db, user_in.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    if not bcrypt.checkpw(user_in.password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    return {"access_token": f"user_id:{user.user_id},user_type:{user.user_type}", "token_type": "bearer"}
