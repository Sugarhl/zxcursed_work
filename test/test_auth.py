from ..main.schemas import UserIn
from ..main.crud import create_user, create_student, create_tutor, get_user_by_username
from ..main.login import create_access_token


def test_register_student(test_app, test_db, test_user_student, test_student):
    with test_db() as db:
        student = create_student(db, UserIn(**test_student.dict()))
        assert student is not None
        assert student.id == test_student.id

        user = create_user(db, UserIn(**test_user_student.dict()), "Student")
        assert user is not None
        assert user.username == test_user_student.username


def test_register_tutor(test_app, test_db, test_user_tutor, test_tutor):
    with test_db() as db:
        tutor = create_tutor(db, UserIn(**test_tutor.dict()))
        assert tutor is not None
        assert tutor.id == test_tutor.id

        user = create_user(db, UserIn(**test_user_tutor.dict()), "Tutor")
        assert user is not None
        assert user.username == test_user_tutor.username


def test_login_student(test_app, test_db, test_user_student):
    with test_db() as db:
        user = get_user_by_username(db, test_user_student.username)
        assert user is not None
        assert user.username == test_user_student.username

        token = create_access_token(user.id, user.user_type)
        assert token is not None


def test_login_tutor(test_app, test_db, test_user_tutor):
    with test_db() as db:
        user = get_user_by_username(db, test_user_tutor.username)
        assert user is not None
        assert user.username == test_user_tutor.username

        token = create_access_token(user.id, user.user_type)
        assert token is not None
