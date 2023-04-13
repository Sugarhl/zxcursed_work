from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.security import OAuth2PasswordBearer
import bcrypt

from server.schemas import UserIn, UserOut
from server.models import User, Student, Tutor
from server.database import get_db
from server.crud import create_user, get_user_by_username, create_student, create_tutor

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def generate_salt() -> str:
    return bcrypt.gensalt().decode("utf-8")


@router.post("/register/{user_type}", response_model=UserOut)
async def register(user_type: str, user_in: UserIn, db: AsyncSession = Depends(get_db)):
    if user_type not in ["Student", "Tutor"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user type")

    existing_user = await get_user_by_username(db, user_in.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Username already exists")

    salt = generate_salt()
    hashed_password = bcrypt.hashpw(
        user_in.password.encode("utf-8"), salt.encode("utf-8"))

    if user_type == "Student":
        new_user = Student(first_name=user_in.first_name,
                           last_name=user_in.last_name, email=user_in.email)
        new_user = await create_student(db, new_user)
    elif user_type == "Tutor":
        new_user = Tutor(first_name=user_in.first_name,
                         last_name=user_in.last_name, email=user_in.email)
        new_user = await create_tutor(db, new_user)

    login_creds = User(user_id=new_user.id, user_type=user_type, username=user_in.username,
                       password=hashed_password.decode("utf-8"))
    db_creds = await create_user(db, login_creds)

    return UserOut(user_id=new_user.id,
                   user_type=db_creds.user_type,
                   username=db_creds.username,
                   first_name=new_user.first_name,
                   last_name=new_user.last_name,
                   email=new_user.email)
