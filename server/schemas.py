from datetime import datetime

from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, constr, validator
import dateutil.parser as parser
import pytz


from server.generation.types import GenType

# auth


class UserIn(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str
# groups


class GroupCreate(BaseModel):
    name: str


class SetStudentToGroup(BaseModel):
    student_id: int
    group_id: int


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    tutor_id: Optional[int] = None

    class Config:
        orm_mode = True


class GroupOut(BaseModel):
    id: int
    name: str
    tutor_id: int

    class Config:
        orm_mode = True


# solutions
class SolutionUpload(BaseModel):
    lab_variant_id: int
    solution_text: Optional[str]
    solution_file: UploadFile


class LabSolutionCommentCreate(BaseModel):
    solution_id: int
    reply_id: Optional[int] = None
    text: str


# labs
class LabCreate(BaseModel):
    lab_name: constr(max_length=255)
    description: str = None
    date_start: Optional[datetime] = None
    deadline: Optional[datetime] = None
    generator_type: GenType

    @validator('date_start', 'deadline', pre=True)
    def parse_datetime(cls, value):
        if isinstance(value, str):
            tz_aware_datetime = parser.isoparse(value)
            utc_datetime = tz_aware_datetime.astimezone(pytz.UTC)
            tz_naive_datetime = utc_datetime.replace(tzinfo=None)
            return tz_naive_datetime
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


# variants
class GenerateParams(BaseModel):
    lab_id: int
