from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import databases
import os

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
DB_FILE = "./test.db"

async_engine = create_engine(DATABASE_URL, echo=True)
async_database = databases.Database(DATABASE_URL)
Base = declarative_base()

# Create a session factory for synchronous operations
sync_engine = create_engine(DATABASE_URL.replace("+aiosqlite", ""), echo=True)

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


def create_database_tables():
    Base.metadata.create_all(sync_engine)


# Check if the database file exists, and create tables if it doesn't
if not os.path.isfile(DB_FILE):
    create_database_tables()
