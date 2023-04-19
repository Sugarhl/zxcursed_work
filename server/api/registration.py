from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from server.models.student import Student
from server.models.tutor import Tutor

from server.schemas import UserIn, UserOut

from server.database import get_db
from server.crud import create_user, get_user_by_username, create_student, create_tutor
from server.utils import UserType

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register/{user_type}", response_model=UserOut)
async def register(user_type: UserType, user_in: UserIn, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_username(db, user_in.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Username already exists")

    if user_type == UserType.STUDENT:
        new_user = Student(first_name=user_in.first_name,
                           last_name=user_in.last_name, email=user_in.email)
        user_id = await create_student(db=db, student=new_user)
    elif user_type == UserType.TUTOR:
        new_user = Tutor(first_name=user_in.first_name,
                         last_name=user_in.last_name, email=user_in.email)
        user_id = await create_tutor(db=db, tutor=new_user)

    await create_user(db=db, user_in=user_in, user_type=user_type.value, user_id=user_id)

    user_out = UserOut(user_id=user_id,
                       user_type=user_type)

    return user_out
