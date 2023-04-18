from fastapi.testclient import TestClient
import pytest
from server.main import app


@pytest.fixture()
def test_app():
    client = TestClient(app)
    yield client
