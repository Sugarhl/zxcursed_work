from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

import databases
# from .config import DATABASE_URL
DATABASE_URL = "postgresql+asyncpg://user:vikisah01@rc1b-8aubff9hb0epodpz.mdb.yandexcloud.net:6432/tasks_manager"
async_engine = create_async_engine(DATABASE_URL,future=True, echo=True)
async_database = databases.Database(DATABASE_URL)

SCHEMA = "lab_management"
Base = declarative_base(metadata=MetaData(schema=SCHEMA))

AsyncSessionFactory = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)


async def get_db():
    async with AsyncSessionFactory() as session:
            yield session
