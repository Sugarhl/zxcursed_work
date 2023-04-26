from datetime import datetime

from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, constr, validator


from server.generation.types import GenType


class UserIn(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str


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


class LabCreate(BaseModel):
    lab_name: constr(max_length=255)
    description: str = None
    date_start: Optional[datetime] = None
    deadline: Optional[datetime] = None
    generator_type: GenType

    @validator('date_start', 'deadline', pre=True)
    def parse_datetime(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value


class LabOut(BaseModel):
    id: int
    lab_name: constr(max_length=255)
    description: Optional[str]
    tutor_id: int
    date_start: Optional[datetime]
    deadline: Optional[datetime]
    generator_type: GenType

    class Config:
        orm_mode = True
