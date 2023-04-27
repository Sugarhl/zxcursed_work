from enum import Enum
import hashlib

import bcrypt
from fastapi import HTTPException, status


class UserType(Enum):
    STUDENT = "student"
    TUTOR = "tutor"


# Some utils
def generate_salt() -> str:
    return bcrypt.gensalt().decode("utf-8")


def generate_salted_password(salt, password):
    salted_password = salt + password
    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
    return hashed_password


async def verify_password(password: str, salt: str, hashed_password: str) -> bool:
    input_hashed_password = generate_salted_password(salt, password)
    return input_hashed_password == hashed_password


def tutor_check(user_type: UserType):
    if user_type != UserType.TUTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only tutors are allowed"
        )
