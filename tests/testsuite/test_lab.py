from datetime import datetime
from httpx import AsyncClient
import pytest

from server.generation.types import GenType
from server.models.lab import Lab
from server.schemas import LabCreate
from fastapi.encoders import jsonable_encoder

pytestmark = pytest.mark.anyio


@pytest.mark.anyio
async def test_lab_create(client: AsyncClient, test_tutor, test_db_session):
    tutor, token = await test_tutor()

    lab_create = LabCreate(
        lab_name="Test Lab",
        description="A test lab",
        date_start=datetime.now(),
        deadline=datetime.now(),
        generator_type=GenType.BASE,
    )

    response = await client.post(
        "lab/create",
        headers={"Authorization": f"Bearer {token}"},
        json=jsonable_encoder(lab_create),
    )

    assert response.status_code == 201

    # Check that the lab was created in the database
    lab_id = response.json()["lab_id"]
    lab_db = test_db_session.get(Lab, lab_id)
    assert lab_db.id == lab_id
    assert lab_db.lab_name == lab_create.lab_name
    assert lab_db.description == lab_create.description
    assert lab_db.date_start == lab_create.date_start
    assert lab_db.deadline == lab_create.deadline
    assert lab_db.tutor_id == tutor.id


@pytest.mark.anyio
async def test_lab_create_negative(client: AsyncClient, test_student, test_tutor):
    _, token = await test_student()

    lab_create = LabCreate(
        lab_name="Test Lab",
        description="A test lab",
        date_start=datetime.now(),
        deadline=datetime.now(),
        generator_type=GenType.BASE,
    )

    response = await client.post(
        "lab/create",
        headers={"Authorization": f"Bearer {token}"},
        json=jsonable_encoder(lab_create),
    )

    assert response.status_code == 403

    _, token = await test_tutor()

    json_data = jsonable_encoder(lab_create)
    json_data["generator_type"] = "SMTH"

    response = await client.post(
        "lab/create", headers={"Authorization": f"Bearer {token}"}, json=json_data
    )

    assert response.status_code == 422
