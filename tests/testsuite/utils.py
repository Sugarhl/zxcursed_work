from enum import Enum
import os
import random
import string
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import json
from datetime import datetime

# Set up the testing database URL
TEST_DATABASE_URL = "postgresql://user:vikisah01@rc1b-8aubff9hb0epodpz.mdb.yandexcloud.net:6432/testing_tasks_manager"

# Set up the testing engine and session factory
test_engine = create_engine(TEST_DATABASE_URL)
test_session_factory = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine, class_=Session)


def generate_random_string(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def swap_files(file1, file2):
    # Generate a random temporary file name
    temp_file = f"temp_{uuid.uuid4().hex}.tmp"

    # Rename file1 to the temporary file
    os.rename(file1, temp_file)

    # Rename file2 to file1
    os.rename(file2, file1)

    # Rename the temporary file to file2
    os.rename(temp_file, file2)
