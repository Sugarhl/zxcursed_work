from datetime import datetime
from httpx import AsyncClient
import pytest

from server.generation.generate import GenType
from server.models.lab import Lab
from server.schemas import LabCreate, LabOut
from fastapi.encoders import jsonable_encoder

from server.utils import UserType

pytestmark = pytest.mark.anyio


@pytest.mark.anyio
async def test_lab_create(
    client: AsyncClient,
    test_tutor,
    test_group_empty,
    test_db_session,
):
    tutor, token = test_tutor()

    group, _ = test_group_empty()

    lab_create = LabCreate(
        lab_name="Test Lab",
        description="A test lab",
        date_start=datetime.now(),
        deadline=datetime.now(),
        group_id=group.id,
        generator_type=GenType.BASE,
    )

    response = await client.post(
        "lab/create",
        headers={"Authorization": f"Bearer {token}"},
        json=jsonable_encoder(lab_create),
    )

    assert response.status_code == 201

    lab_id = response.json()["lab_id"]
    lab_db = test_db_session.get(Lab, lab_id)
    assert lab_db.id == lab_id
    assert lab_db.lab_name == lab_create.lab_name
    assert lab_db.description == lab_create.description
    assert lab_db.date_start == lab_create.date_start
    assert lab_db.deadline == lab_create.deadline
    assert lab_db.tutor_id == tutor.id


@pytest.mark.anyio
async def test_lab_create_student_access(
    client: AsyncClient, test_student, test_group_empty
):
    _, token = test_student()
    group, _ = test_group_empty()

    lab_create = LabCreate(
        lab_name="Test Lab",
        description="A test lab",
        date_start=datetime.now(),
        deadline=datetime.now(),
        group_id=group.id,
        generator_type=GenType.BASE,
    )

    response = await client.post(
        "lab/create",
        headers={"Authorization": f"Bearer {token}"},
        json=jsonable_encoder(lab_create),
    )

    assert response.status_code == 403


@pytest.mark.anyio
async def test_lab_create_incorrect_input(
    client: AsyncClient, test_group_empty, test_tutor
):
    _, token = test_tutor()

    group, _ = test_group_empty()

    lab_create = LabCreate(
        lab_name="Test Lab",
        description="A test lab",
        date_start=datetime.now(),
        deadline=datetime.now(),
        group_id=group.id,
        generator_type=GenType.BASE,
    )
    raw_data = jsonable_encoder(lab_create)

    raw_data["generator_type"] = "SMTH"

    response = await client.post(
        "lab/create",
        headers={"Authorization": f"Bearer {token}"},
        json=raw_data,
    )

    assert response.status_code == 422

    raw_data["generator_type"] = GenType.BASE.value
    raw_data["deadline"] = "SMTH_DATE"

    response = await client.post(
        "lab/create",
        headers={"Authorization": f"Bearer {token}"},
        json=raw_data,
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_lab_create_non_exist_group(client: AsyncClient, test_tutor):
    _, token = test_tutor()
    lab_create = LabCreate(
        lab_name="Test Lab",
        description="A test lab",
        date_start=datetime.now(),
        deadline=datetime.now(),
        group_id=123,
        generator_type=GenType.BASE,
    )

    response = await client.post(
        "lab/create",
        headers={"Authorization": f"Bearer {token}"},
        json=jsonable_encoder(lab_create),
    )

    assert response.status_code == 404


@pytest.mark.anyio
async def test_get_student_labs(client: AsyncClient, test_vars_with_group, get_token):
    lab, _, students, _ = await test_vars_with_group()

    for student in students:
        student_token = get_token(student.id, UserType.STUDENT)

        response = await client.get(
            "lab/get/student/all", headers={"Authorization": f"Bearer {student_token}"}
        )

        assert response.status_code == 200
        student_labs = [LabOut(**variant) for variant in response.json()]
        assert len(student_labs) == 1


@pytest.mark.anyio
async def test_get_student_labs_negative(
    client: AsyncClient, test_vars_with_group, get_token, test_student
):
    lab, tutor, students, _ = await test_vars_with_group()

    for student in students:

        invalid_token = "invalid_token"
        response = await client.get(
            "lab/get/student/all", headers={"Authorization": f"Bearer {invalid_token}"}
        )
        assert response.status_code == 401

        tutor_token = get_token(tutor.id, UserType.TUTOR)
        response = await client.get(
            "lab/get/student/all", headers={"Authorization": f"Bearer {tutor_token}"}
        )
        assert response.status_code == 403

        _, empty_student_token = test_student()
        response = await client.get(
            "lab/get/student/all",
            headers={"Authorization": f"Bearer {empty_student_token}"},
        )
        assert response.status_code == 200
        student_labs = [LabOut(**variant) for variant in response.json()]
        assert len(student_labs) == 0


@pytest.mark.anyio
async def test_get_tutor_labs(client: AsyncClient, test_vars_with_group, get_token):
    lab, tutor, students, _ = await test_vars_with_group()

    token = get_token(tutor.id, UserType.TUTOR)

    response = await client.get(
        "lab/get/tutor/all", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    labs = [LabOut(**variant) for variant in response.json()]
    assert len(labs) == 1
