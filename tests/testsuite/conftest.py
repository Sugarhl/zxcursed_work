from server.utils import generate_salt, generate_salted_password
import asyncio
import random
import string
from fastapi.testclient import TestClient
import pytest

from server.main import app
from server.schemas import UserIn
from server.models import Student, User
from server.crud import create_student, create_user
from server.utils import UserType
import server.config as con
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Set up the testing database URL
TEST_DATABASE_URL = "postgresql://user:vikisah01@rc1b-8aubff9hb0epodpz.mdb.yandexcloud.net:6432/testing_tasks_manager"

# Set up the testing engine and session factory
test_engine = create_engine(TEST_DATABASE_URL)
test_session_factory = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine, class_=Session)


@pytest.fixture(scope="module")
def client():
    client = TestClient(app)
    return client


def generate_random_string(length=6):
    return ''.join(random.choices(string.ascii_letters
                                  + string.digits, k=length))


@pytest.fixture(scope="function")
def test_user():
    unique_id = f"{generate_random_string()}"
    test_user = UserIn(username=f"teststudent_{unique_id}",
                       password="testpassword",
                       first_name="Test",
                       last_name="Student",
                       email=f"test_{unique_id}@example.com")
    return test_user


@pytest.fixture(scope="module")
def test_db_session():
    with test_session_factory() as session:
        yield session


@pytest.fixture(scope="function")
async def test_student(test_user, test_db_session):
    new_student = Student(first_name=test_user.first_name,
                          last_name=test_user.last_name, email=test_user.email)

    # Add the new student to the session
    test_db_session.add(new_student)
    test_db_session.commit()

    student_id = new_student.id

    # Create a new user
    salt = generate_salt()
    salted_password = generate_salted_password(salt, test_user.password)

    user = User(username=test_user.username,
                salt=salt,
                password=salted_password,
                user_type=UserType.STUDENT.value,
                user_id=student_id)

    # Add the new user to the session
    test_db_session.add(user)
    test_db_session.commit()

    return student_id, test_user
