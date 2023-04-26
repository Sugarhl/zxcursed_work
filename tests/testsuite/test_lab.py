from datetime import datetime
import json
from httpx import AsyncClient
import pytest

from server.CRUD.lab import get_lab
from server.generation.types import GenType
from server.models.lab import Lab
from server.schemas import LabCreate
from tests.testsuite.utils import JSONEncoderWithDatetime

pytestmark = pytest.mark.anyio


@pytest.mark.anyio
async def test_login_for_access_token(client: AsyncClient, test_tutor, test_db_session):

    assert test_tutor

    lab_create = LabCreate(
        lab_name="Test Lab",
        description="A test lab",
        date_start=datetime(2023, 5, 1),
        deadline=datetime(2023, 5, 8),
        generator_type=GenType.BASE,
    )

    json_data = json.dumps(lab_create.dict(), cls=JSONEncoderWithDatetime)

    response = await client.post("/create_lab", headers={"Authorization": "Bearer test_token"},
                                 json=json_data)
    assert response.status_code == 201

    # Check that the lab was created in the database
    lab_id = response.json()["lab_id"]
    lab_db = await get_lab(test_db_session, lab_id)
    assert lab_db.id == lab_id
    assert lab_db.lab_name == lab_create.lab_name
    assert lab_db.description == lab_create.description
    assert lab_db.file_of_lab == lab_create.file_of_lab
    assert lab_db.date_start.isoformat() == lab_create.date_start
    assert lab_db.deadline.isoformat() == lab_create.deadline
    assert lab_db.tutor_id == test_tutor.id
