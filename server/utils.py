from enum import Enum
import hashlib

import bcrypt


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
