import random
import string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


# Set up the testing database URL
TEST_DATABASE_URL = "postgresql://user:vikisah01@rc1b-8aubff9hb0epodpz.mdb.yandexcloud.net:6432/testing_tasks_manager"

# Set up the testing engine and session factory
test_engine = create_engine(TEST_DATABASE_URL)
test_session_factory = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine, class_=Session
)


def generate_random_string(length=6):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))
