import random
import string
from server.schemas import UserIn
from server.modelss import Student, Tutor
from server.crud import create_student, create_tutor, create_user
from server.utils import UserType
from sqlalchemy.ext.asyncio import AsyncSession


def generate_random_string(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def make_user_in():
    unique_id = f"{generate_random_string()}"
    test_user = UserIn(username=f"teststudent_{unique_id}", password="testpassword",
                       first_name="Test", last_name="Student", email=f"test_{unique_id}@example.com")
    return test_user
