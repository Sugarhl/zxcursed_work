import random
import string
from server.schemas import UserIn
from server.models import Student, Tutor
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


async def make_student(session):
    test_user = make_user_in()
    new_student = Student(first_name=test_user.first_name,
                          last_name=test_user.last_name, email=test_user.email)
    student_id = await create_student(db=session, student=new_student)
    await create_user(db=session, user_in=test_user, user_type=UserType.STUDENT.value, user_id=student_id)
    yield student_id, test_user
