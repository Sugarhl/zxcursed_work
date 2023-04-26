import subprocess
import pytest

from httpx import AsyncClient
from server.main import app

from server.models.base import Base
from server.database import async_engine
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
        ["uvicorn", "myapp.main:app", "--host",
            "localhost", "--port", "8000", "--reload"],
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


@pytest.fixture(scope="function")
def test_student_in():
    unique_id = f"{generate_random_string()}"
    test_user = UserIn(username=f"teststudent_{unique_id}",
                       password="testpassword",
                       first_name="Test",
                       last_name="Student",
                       email=f"test_{unique_id}@example.com")
    return test_user


@pytest.fixture(scope="function")
def test_tutor_in():
    unique_id = f"{generate_random_string()}"
    test_user = UserIn(username=f"test_tutor_{unique_id}",
                       password="testpassword",
                       first_name="Test",
                       last_name="Tutor",
                       email=f"test_{unique_id}@example.com")
    return test_user


@pytest.fixture(scope="function")
def test_db_session():
    with test_session_factory() as session:
        yield session


@pytest.fixture(scope="function")
async def test_student(test_student_in, test_db_session):
    new_student = Student(first_name=test_student_in.first_name,
                          last_name=test_student_in.last_name, email=test_student_in.email)

    # Add the new student to the session
    test_db_session.add(new_student)
    test_db_session.commit()

    student_id = new_student.id

    # Create a new user
    salt = generate_salt()
    salted_password = generate_salted_password(salt, test_student_in.password)

    user = User(username=test_student_in.username,
                salt=salt,
                password=salted_password,
                user_type=UserType.STUDENT,
                user_id=student_id)

    # Add the new user to the session
    test_db_session.add(user)
    test_db_session.commit()

    token = create_access_token(user_id=user.user_id, user_type=user.user_type)

    return test_student_in, token.access_token, user


@pytest.fixture(scope="function")
async def test_tutor(test_tutor_in, test_db_session):
    new_tutor = Tutor(first_name=test_tutor_in.first_name,
                      last_name=test_tutor_in.last_name, email=test_tutor_in.email)

    # Add the new student to the session
    test_db_session.add(new_tutor)
    test_db_session.commit()

    student_id = new_tutor.id

    # Create a new user
    salt = generate_salt()
    salted_password = generate_salted_password(salt, test_tutor_in.password)

    user = User(username=test_tutor_in.username,
                salt=salt,
                password=salted_password,
                user_type=UserType.TUTOR,
                user_id=student_id)

    # Add the new user to the session
    test_db_session.add(user)
    test_db_session.commit()

    token = create_access_token(user_id=user.user_id, user_type=user.user_type)

    return test_tutor_in, token.access_token, user
