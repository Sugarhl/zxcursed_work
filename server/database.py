from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

from sqlalchemy.pool import NullPool
import databases
from server.models.base import Base

from server.models.lab_variant import LabVariant
from server.models.lab import Lab
from server.models.lab_solution import LabSolution
from server.models.lab_result import LabResult
from server.models.lab_solution_comment import LabSolutionComment
from server.models.student import Student
from server.models.tutor import Tutor
from server.models.user import User

from server.config import DATABASE_URL

SCHEMA = "lab_management"

async_engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_database = databases.Database(DATABASE_URL)

session_factory = sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=async_engine, class_=AsyncSession)


async def get_db():
    async with session_factory() as session:
        yield session


tables = [
    Lab,
    LabVariant,
    LabSolution,
    LabResult,
    LabSolutionComment,
    Student,
    Tutor,
    User
]


async def create_tables():
    async with async_engine.begin() as conn:

        # Create tables without foreign key dependencies
        await conn.run_sync(User.__table__.create, checkfirst=True)
        await conn.run_sync(Student.__table__.create, checkfirst=True)
        await conn.run_sync(Tutor.__table__.create, checkfirst=True)
        await conn.run_sync(Lab.__table__.create, checkfirst=True)

        # Create tables with foreign key dependencies
        await conn.run_sync(LabVariant.__table__.create, checkfirst=True)
        await conn.run_sync(LabSolution.__table__.create, checkfirst=True)
        await conn.run_sync(LabResult.__table__.create, checkfirst=True)
        await conn.run_sync(LabSolutionComment.__table__.create, checkfirst=True)
