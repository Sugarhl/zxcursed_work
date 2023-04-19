import pytest


@pytest.mark.asyncio
async def test_login_for_access_token(client,  test_user, test_student):

    student_id, _ = await test_student

    response = client.post("/auth/token", data={
        "username": test_user.username,
        "password": test_user.password
    })

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
