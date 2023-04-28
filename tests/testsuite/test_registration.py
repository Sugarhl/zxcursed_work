import json
import pytest
from server.utils import UserType


from server.token import decode_access_token


pytestmark = pytest.mark.anyio


async def test_register_student(client, test_student_in):
    response = await client.post(
        "/registration/register/student", json=test_student_in().dict()
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"
    recieved_token = response.json()["access_token"]
    user_id, user_type = decode_access_token(token=recieved_token)
    assert user_id
    assert user_type == UserType.STUDENT


async def test_register_tutor(client, test_tutor_in):
    response = await client.post(
        "/registration/register/tutor", json=test_tutor_in().dict()
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"
    recieved_token = response.json()["access_token"]
    user_id, user_type = decode_access_token(token=recieved_token)
    assert user_id
    assert user_type == UserType.TUTOR
