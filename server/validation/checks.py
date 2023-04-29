from fastapi import HTTPException, status

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


# Access checks
def tutor_access_check(user_type: UserType):
    if user_type != UserType.TUTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only tutors are allowed"
        )


def group_check_access(group, tutor):
    if group.tutor_id != tutor.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this group",
        )
