from fastapi import HTTPException, UploadFile, status
from server.models import group
from server.models.student import Student
from server.models.tutor import Tutor
from server.models.lab_variant import LabVariant

from server.utils import UserType


def user_check(user):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Non - existent credentials",
        )


def student_check(student):
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student does not exist"
        )


def tutor_check(tutor):
    if not tutor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tutor does not exist"
        )


def lab_check(lab):
    if not lab:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lab does not exist"
        )


def group_check(group):
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group does not exist",
        )


def lab_variant_check(lab_variant):
    if not lab_variant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lab variant does not exist",
        )


def solution_check(file):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solution not found",
        )


def file_check(file):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )


# Access checks
def tutor_access_check(user_type: UserType):
    if user_type != UserType.TUTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only tutors are allowed"
        )


def student_access_check(user_type: UserType):
    if user_type != UserType.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only students are allowed"
        )


def group_check_access(group: group.Group, tutor: Tutor):
    if group.tutor_id != tutor.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this group",
        )


def lab_var_check_access(lab_variant: LabVariant, student: Student):
    if lab_variant.student_id != student.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to lab variant",
        )


def file_ext_check(file: UploadFile):
    if not file.filename.endswith(".ipynb"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Only .ipynb files are supported.",
        )
