import os
import random
import string
from typing import List
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from server.generation.base import Variant

from server.models.lab import Lab
from server.models.lab_variant import LabVariant
from server.models.student import Student


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


def assign_variants(
    lab: Lab, variants: List[Variant], students: List[Student], db: Session
) -> List[LabVariant]:
    assert len(variants) == len(students)
    lab_vars = []

    for i, variant in enumerate(variants):
        lab_variant = LabVariant(
            lab_id=lab.id,
            student_id=students[i].id,
            variant_number=i,
            variant_filename=variant.file_name,
            file_key=variant.key,
        )
        db.add(lab_variant)
        db.commit()
        lab_vars.append(lab_variant)

    return lab_vars
