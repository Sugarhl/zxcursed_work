import re

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from server.schemas import UserIn
from server.utils import UserType
from server.CRUD.user import get_user_by_email, get_user_by_username


async def check_user_exists(db: AsyncSession, user_type: UserType, user_in: UserIn):
    existing_user = await get_user_by_username(db, user_in.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Username already exists")

    existing_user = await get_user_by_email(db, email=user_in.email, user_type=user_type)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email already in use")


def validate_user_data(user_type: UserType, user_in: UserIn):
    # Validate user_type
    if user_type not in [UserType.STUDENT, UserType.TUTOR]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid user type")

    # Validate user_in
    if not user_in.username or len(user_in.username) > 50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid username")
    if not user_in.email or not re.match(r"[^@]+@[^@]+\.[^@]+", user_in.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid email")
    if not user_in.first_name or len(user_in.first_name) > 50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid first name")
    if not user_in.last_name or len(user_in.last_name) > 50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid last name")
