from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import databases

TESTING = True

if TESTING:
    DATABASE_URL = "sqlite+aiosqlite:///./test.db"
else:
    DATABASE_URL = "postgresql+asyncpg://username:password@localhost/db_name"

async_engine = create_engine(DATABASE_URL, echo=True)
async_database = databases.Database(DATABASE_URL)
Base = declarative_base()

# Create a session factory for synchronous operations
if TESTING:
    sync_engine = create_engine(DATABASE_URL.replace("aiosqlite", "sqlite"), echo=True)
else:
    sync_engine = create_engine(DATABASE_URL.replace("asyncpg", "psycopg2"), echo=True)

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
