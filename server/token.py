import datetime
from typing import Tuple
import uuid

import jwt
from fastapi import HTTPException, status
from server.CRUD.student import get_student_by_id
from server.CRUD.tutor import get_tutor_by_id
from server.CRUD.user import get_user_by_id
from jwt import ExpiredSignatureError, InvalidTokenError
from server.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from server.models.user import User
from server.schemas import Token
from server.utils import UserType

from sqlalchemy.ext.asyncio import AsyncSession


def create_access_token(user_id: uuid.UUID, user_type: UserType) -> Token:
    expire = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {
        "user_id": str(user_id),
        "user_type": user_type.value,
        "exp": expire,
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return Token(access_token=encoded_jwt, token_type="bearer")


def decode_access_token(token: str) -> Tuple[int, UserType]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = uuid.UUID(payload.get("user_id"))
        user_type_str = payload.get("user_type")
        user_type = UserType(user_type_str)
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        # Check if the token has expired
        now = datetime.datetime.utcnow()
        expiration_datetime = datetime.datetime.fromtimestamp(payload["exp"])
        if now >= expiration_datetime:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )

        return user_id, user_type
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user type in token",
        )


async def auth_by_token(db: AsyncSession, token: str) -> User:
    user_id, user_type = decode_access_token(token)

    user = await get_user_by_id(db=db, user_id=user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Non - existent credentials",
        )

    if user_type == UserType.STUDENT:
        student = await get_student_by_id(db=db, user_id=user.user_id)
        return student, user_type

    elif user_type == UserType.TUTOR:
        tutor = await get_tutor_by_id(db=db, user_id=user.user_id)
        return tutor, user_type

    return user, user_type
