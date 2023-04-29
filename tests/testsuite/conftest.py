from datetime import datetime
import subprocess
import pytest

from httpx import AsyncClient
from server.generation.types import GenType
from server.main import app

from server.models.base import Base
from server.database import async_engine
from server.models.group import Group
from server.models.lab import Lab
from server.models.tutor import Tutor
from server.models.user import User
from server.token import create_access_token

from server.utils import UserType, generate_salt, generate_salted_password
from server.schemas import UserIn
from server.models.student import Student
import server.config as config
from tests.testsuite.utils import generate_random_string, test_session_factory


@pytest.fixture(
    params=[
        pytest.param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop"),
    ]
)
def anyio_backend(request):
    return request.param


async def start_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await async_engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def run_server():
    config.testig_mode = True
    proc = subprocess.Popen(
        [
            "uvicorn",
            "myapp.main:app",
            "--host",
            "localhost",
            "--port",
            "8000",
            "--reload",
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        yield
    finally:
        proc.stdin.close()
        proc.stdout.close()
        proc.stderr.close()
        proc.terminate()
        proc.wait()


@pytest.fixture
async def client(run_server) -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url="http://localhost:8000",
    ) as client:
        await start_db()
        yield client
        # for AsyncEngine created in function scope, close and
        # clean-up pooled connections
        await async_engine.dispose()


@pytest.fixture
def test_student_in():
    def do_test_student_in():
        unique_id = f"{generate_random_string()}"
        test_user = UserIn(
            username=f"teststudent_{unique_id}",
            password="testpassword",
            first_name="Test",
            last_name="Student",
            email=f"test_{unique_id}@example.com",
        )
        return test_user

    return do_test_student_in


@pytest.fixture
def test_tutor_in():
    def do_test_tutor_in():
        unique_id = f"{generate_random_string()}"
        test_user = UserIn(
            username=f"test_tutor_{unique_id}",
            password="testpassword",
            first_name="Test",
            last_name="Tutor",
            email=f"test_{unique_id}@example.com",
        )
        return test_user

    return do_test_tutor_in


@pytest.fixture
def test_db_session():
    with test_session_factory() as session:
        yield session


@pytest.fixture
def test_student(test_student_in, test_db_session):
    def do_test_student():
        student = test_student_in()
        new_student = Student(
            first_name=student.first_name,
            last_name=student.last_name,
            email=student.email,
        )

        # Add the new student to the session
        test_db_session.add(new_student)
        test_db_session.commit()

        student_id = new_student.id

        # Create a new user
        salt = generate_salt()
        salted_password = generate_salted_password(salt, student.password)

        user = User(
            username=student.username,
            salt=salt,
            password=salted_password,
            user_type=UserType.STUDENT,
            user_id=student_id,
        )

        # Add the new user to the session
        test_db_session.add(user)
        test_db_session.commit()

        token = create_access_token(user_id=user.id, user_type=user.user_type)

        return new_student, token.access_token

    return do_test_student


@pytest.fixture
def test_student_creds(test_student_in, test_db_session):
    def do_test_student_creds():
        student = test_student_in()
        new_student = Student(
            first_name=student.first_name,
            last_name=student.last_name,
            email=student.email,
        )

        # Add the new student to the session
        test_db_session.add(new_student)
        test_db_session.commit()

        student_id = new_student.id

        # Create a new user
        salt = generate_salt()
        salted_password = generate_salted_password(salt, student.password)

        user = User(
            username=student.username,
            salt=salt,
            password=salted_password,
            user_type=UserType.STUDENT,
            user_id=student_id,
        )

        # Add the new user to the session
        test_db_session.add(user)
        test_db_session.commit()

        token = create_access_token(user_id=user.id, user_type=user.user_type)

        return student, token.access_token, user

    return do_test_student_creds


@pytest.fixture
def test_tutor(test_tutor_in, test_db_session):
    def do_test_tutor():
        tutor = test_tutor_in()
        new_tutor = Tutor(
            first_name=tutor.first_name,
            last_name=tutor.last_name,
            email=tutor.email,
        )

        # Add the new student to the session
        test_db_session.add(new_tutor)
        test_db_session.commit()

        student_id = new_tutor.id

        # Create a new user
        salt = generate_salt()
        salted_password = generate_salted_password(salt, tutor.password)

        user = User(
            username=tutor.username,
            salt=salt,
            password=salted_password,
            user_type=UserType.TUTOR,
            user_id=student_id,
        )

        # Add the new user to the session
        test_db_session.add(user)
        test_db_session.commit()

        token = create_access_token(user_id=user.id, user_type=user.user_type)

        return new_tutor, token.access_token

    return do_test_tutor


@pytest.fixture
def test_group(test_tutor, test_student, test_db_session):
    def do_test_group():
        tutor, _ = test_tutor()
        group = Group(name="TEST GROUP", tutor_id=tutor.id)
        test_db_session.add(group)
        test_db_session.commit()

        student, _ = test_student()

        return group, tutor, student

    return do_test_group


def test_lab(test_db_session):
    def do_test_lab():
        unique_str = generate_random_string()

        lab = Lab(
            lab_name=f"Test Lab {unique_str}",
            description=f"A test lab number {unique_str}",
            date_start=datetime.now(),
            deadline=datetime.now(),
            generator_type=GenType.BASE,
        )
        test_db_session.add(lab)
        test_db_session.commit()

        return lab

    return do_test_lab
