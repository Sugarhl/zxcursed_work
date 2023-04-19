import json
import pytest

from tests.testsuite.utils import make_user_in


@pytest.mark.asyncio
async def test_register(client):
    test_user = make_user_in()

    response = client.post(
        "/registration/register/student", json=test_user.dict())

    assert response.status_code == 200
    assert "user_id" in response.json()
    assert "user_type" in response.json()
    assert response.json()["user_type"] == "student"
