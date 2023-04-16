import datetime
from typing import Dict, Optional, Union

import jwt
from fastapi import HTTPException, status
from jwt import ExpiredSignatureError, InvalidTokenError
from server.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


def create_access_token(user_id: int, user_type: str) -> str:
    expire = datetime.datetime.utcnow(
    ) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"user_id": user_id, "user_type": user_type, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(encoded_jwt)
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Union[int, str]]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        user_type = payload.get("user_type")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        # Check if the token has expired
        now = datetime.datetime.utcnow()
        expiration_datetime = datetime.datetime.fromtimestamp(payload["exp"])
        if now >= expiration_datetime:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

        return user_id, user_type
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
