import pytest

from server.database import session_factory
from tests.testsuite.utils import make_student


@pytest.mark.asyncio
async def test_login_for_access_token(test_app):
    async with session_factory() as session:
        _, test_user = await make_student(session=session)

        response = test_app.post("/auth/token", data={
            "username": test_user.username,
            "password": test_user.password
        })

        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "token_type" in response.json()
