from httpx import AsyncClient
import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.anyio
async def test_login_for_access_token(client: AsyncClient, test_student):

    assert test_student

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'username': f'{test_student.username}',
        'password': f'{test_student.password}',
    }

    response = await client.post("/auth/token", headers=headers, data=data)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"
