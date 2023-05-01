from httpx import AsyncClient
import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.anyio
async def test_login_for_access_token(client: AsyncClient, test_student_creds):
    student, token, _ = test_student_creds()

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "username": f"{student.username}",
        "password": f"{student.password}",
    }

    response = await client.post("/auth/token", headers=headers, data=data)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"] == token


@pytest.mark.anyio
async def test_login_not_exists(client: AsyncClient):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "username": "not_exists",
        "password": "not_exists",
    }

    response = await client.post("/auth/token", headers=headers, data=data)

    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == "Incorrect username or password"
