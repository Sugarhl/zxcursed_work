import os
import random
import string
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


load_dotenv(dotenv_path=".env.test")

# Set up the testing database URL
TEST_DATABASE_URL = os.getenv("SYNC_DATABASE_URL", "TESTING_DB")

# Set up the testing engine and session factory
test_engine = create_engine(TEST_DATABASE_URL)
test_session_factory = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine, class_=Session
)


def generate_random_string(length=6):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))
