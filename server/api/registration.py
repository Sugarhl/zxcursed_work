from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from server.models.student import Student
from server.models.tutor import Tutor

from server.schemas import UserIn, Token

from server.database import get_db

from server.CRUD.user import create_user
from server.CRUD.student import create_student
from server.CRUD.tutor import create_tutor

from server.token import create_access_token
from server.utils import UserType
from server.validation.registration import check_user_exists, validate_user_data

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.post("/register/{user_type}", response_model=Token)
async def register(user_type: UserType, user_in: UserIn, db: AsyncSession = Depends(get_db)):
    validate_user_data(user_type=user_type, user_in=user_in)

    await check_user_exists(db=db, user_type=user_type, user_in=user_in)

    if user_type == UserType.STUDENT:
        new_user = Student(first_name=user_in.first_name,
                           last_name=user_in.last_name, email=user_in.email)
        try:
            user_id = await create_student(db=db, student=new_user)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Bad student data")
    elif user_type == UserType.TUTOR:
        new_user = Tutor(first_name=user_in.first_name,
                         last_name=user_in.last_name, email=user_in.email)
        try:
            user_id = await create_tutor(db=db, tutor=new_user)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Bad tutor data")

    try:
        user_id = await create_user(db=db, user_in=user_in, user_type=user_type, user_id=user_id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Bad credetials")

    return create_access_token(user_id, user_type)
