from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel

from server.utils import UserType


class UserIn(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str


class UserOut(BaseModel):
    user_id: int
    user_type: UserType


class Config:
    orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class SolutionUpload(BaseModel):
    lab_variant_id: int
    solution_text: Optional[str]
    solution_file: UploadFile


class LabSolutionCommentCreate(BaseModel):
    solution_id: int
    reply_id: Optional[int] = None
    text: str
