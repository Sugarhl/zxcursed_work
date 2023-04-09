import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..main.main import app
from ..main.database import Base
from ..main.models import User, Student, Tutor

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="module")
def test_db():
    yield TestingSessionLocal


@pytest.fixture
def test_user_student():
    return User(
        user_id=1,
        user_type="Student",
        username="test_student",
        password="test_password",
    )


@pytest.fixture
def test_student():
    return Student(
        id=1,
        first_name="Test",
        last_name="Student",
        email="test_student@example.com",
    )


@pytest.fixture
def test_user_tutor():
    return User(
        user_id=1,
        user_type="Tutor",
        username="test_tutor",
        password="test_password",
    )


@pytest.fixture
def test_tutor():
    return Tutor(
        id=1,
        first_name="Test",
        last_name="Tutor",
        email="test_tutor@example.com",
    )
