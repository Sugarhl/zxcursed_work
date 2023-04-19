from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
import databases

from server.config import DATABASE_URL

SCHEMA = "lab_management"
Base = declarative_base(metadata=MetaData(schema=SCHEMA))

async_engine = create_async_engine(DATABASE_URL, echo=True)
async_database = databases.Database(DATABASE_URL)

session_factory = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)


async def get_db():
    async with session_factory() as session:
        yield session
