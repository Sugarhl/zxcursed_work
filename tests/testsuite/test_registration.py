import json
import pytest
from server.models import Student

from server.schemas import LabSolutionCommentCreate, UserIn
from server.utils import UserType
from server.database import session_factory
from tests.testsuite.utils import make_user_in


@pytest.mark.asyncio
async def test_register(test_app):
    test_user = make_user_in()

    response = test_app.post(
        "/registration/register/student", json=test_user.dict())

    assert response.status_code == 200
    assert "user_id" in response.json()
    assert "user_type" in response.json()
    assert response.json()["user_type"] == "student"
