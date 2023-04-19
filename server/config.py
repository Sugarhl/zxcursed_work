from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "YOUR_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

SCHEMA = 'lab_management'
TESTING_MODE = False

PROD_DB = "postgresql+asyncpg://user:vikisah01@rc1b-8aubff9hb0epodpz.mdb.yandexcloud.net:6432/tasks_manager"

TESTING_DB = "postgresql+asyncpg://user:vikisah01@rc1b-8aubff9hb0epodpz.mdb.yandexcloud.net:6432/testing_tasks_manager"


DATABASE_URL = TESTING_DB if TESTING_MODE else PROD_DB

# DATABASE_URL = os.getenv(
#     "DATABASE_URL", "postgresql+asyncpg://user:vikisah01@rc1b-8aubff9hb0epodpz.mdb.yandexcloud.net:6432/tasks_manager")
