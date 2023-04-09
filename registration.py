from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.security import OAuth2PasswordBearer
import bcrypt

from schemas import UserIn, UserOut
from models import User, Student, Tutor
from database import async_engine
from crud import create_user, get_user_by_username

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


async def async_session_manager():
    async with async_session() as s:
        yield s


def generate_salt() -> str:
    return bcrypt.gensalt().decode("utf-8")


@router.post("/register/{user_type}", response_model=UserOut)
async def register(user_type: str, user_in: UserIn, db: AsyncSession = Depends(async_session)):
    if user_type not in ["Student", "Tutor"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user type")

    existing_user = await get_user_by_username(db, user_in.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    salt = generate_salt()
    hashed_password = bcrypt.hashpw(user_in.password.encode("utf-8"), salt.encode("utf-8"))

    if user_type == "Student":
        new_user = Student(first_name=user_in.first_name, last_name=user_in.last_name, email=user_in.email)
    elif user_type == "Tutor":
        new_user = Tutor(first_name=user_in.first_name, last_name=user_in.last_name, email=user_in.email)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    login_creds = User(user_id=new_user.id, user_type=user_type, username=user_in.username,
                       password=hashed_password.decode("utf-8"))
    return await create_user(db, login_creds)
