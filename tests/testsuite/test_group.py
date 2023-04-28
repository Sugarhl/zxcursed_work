from server.models.student import Student
from server.schemas import GroupCreate, GroupUpdate, SetStudentToGroup
from httpx import AsyncClient
import pytest
from server.models.group import Group

from fastapi.encoders import jsonable_encoder

pytestmark = pytest.mark.anyio


@pytest.mark.anyio
async def test_create_group(client: AsyncClient, test_tutor, test_db_session):
    tutor, token = await test_tutor()

    group_create = GroupCreate(name="Test Group", tutor_id=tutor.id)

    response = await client.post(
        "/group/create",
        headers={"Authorization": f"Bearer {token}"},
        json=jsonable_encoder(group_create),
    )

    assert response.status_code == 201

    # Check that the group was created in the database
    group_id = response.json()["group_id"]
    group_db = test_db_session.get(Group, group_id)
    assert group_db.id == group_id
    assert group_db.name == group_create.name
    assert group_db.tutor_id == tutor.id


@pytest.mark.anyio
async def test_create_group_negative(client: AsyncClient, test_student):
    _, token = await test_student()

    group_create = GroupCreate(
        name="Test Group",
    )

    response = await client.post(
        "/group/create",
        headers={"Authorization": f"Bearer {token}"},
        json=jsonable_encoder(group_create),
    )

    assert response.status_code == 403


@pytest.mark.anyio
async def test_get_group(client: AsyncClient, test_tutor):
    tutor, token = await test_tutor()

    group_create = GroupCreate(name="Test Group", tutor_id=tutor.id)

    response = await client.post(
        "/group/create",
        headers={"Authorization": f"Bearer {token}"},
        json=jsonable_encoder(group_create),
    )
    group_id = response.json()["group_id"]

    response = await client.get(
        f"/group/get/{group_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == group_id
    assert response.json()["name"] == group_create.name
    assert response.json()["tutor_id"] == tutor.id


@pytest.mark.anyio
async def test_get_group_negative(client: AsyncClient, test_student):
    _, token = await test_student()

    response = await client.get(
        f"/group/get/{100}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


@pytest.mark.anyio
async def test_update_group_name(client: AsyncClient, test_tutor, test_db_session):
    _, token = await test_tutor()

    group_create = GroupCreate(name="Test Group")

    response = await client.post(
        "/group/create",
        headers={"Authorization": f"Bearer {token}"},
        json=jsonable_encoder(group_create),
    )
    group_id = response.json()["group_id"]

    group_update = GroupUpdate(name="Updated Test Group")

    response = await client.put(
        f"/group/update/{group_id}",
        headers={"Authorization": f"Bearer {token}"},
        json=jsonable_encoder(group_update),
    )

    assert response.status_code == 204

    group_db = test_db_session.get(Group, group_id)
    assert group_db.id == group_id
    assert group_db.name == group_update.name


@pytest.mark.anyio
async def test_update_group_tutor(client: AsyncClient, test_tutor, test_db_session):
    _, token = await test_tutor()
    new_tutor, _ = await test_tutor()

    group_create = GroupCreate(name="Test Group")

    response = await client.post(
        "/group/create",
        headers={"Authorization": f"Bearer {token}"},
        json=jsonable_encoder(group_create),
    )
    group_id = response.json()["group_id"]

    group_update = GroupUpdate(name="Updated Test Group", tutor_id=new_tutor.id)

    response = await client.put(
        f"/group/update/{group_id}",
        headers={"Authorization": f"Bearer {token}"},
        json=jsonable_encoder(group_update),
    )

    assert response.status_code == 204

    group_db = test_db_session.get(Group, group_id)
    assert group_db.id == group_id
    assert group_db.name == group_update.name
    assert group_db.tutor_id == group_update.tutor_id


@pytest.mark.anyio
async def test_update_group_negative(client: AsyncClient, test_student, test_tutor):
    tutor, token = await test_tutor()

    group_create = GroupCreate(name="Test Group")

    response = await client.post(
        "/group/create",
        headers={"Authorization": f"Bearer {token}"},
        json=jsonable_encoder(group_create),
    )

    group_id = response.json()["group_id"]

    _, token = await test_student()

    group_update = GroupUpdate(
        name="Updated Test Group",
    )

    response = await client.put(
        f"/group/update/{group_id}",
        headers={"Authorization": f"Bearer {token}"},
        json=jsonable_encoder(group_update),
    )
    assert response.status_code == 403

    tutor, token = await test_tutor()

    response = await client.put(
        f"/group/update/{group_id}",
        headers={"Authorization": f"Bearer {token}"},
        json=jsonable_encoder(group_update),
    )
    assert response.status_code == 403

    response = await client.put(
        f"/group/update/{232323}",
        headers={"Authorization": f"Bearer {token}"},
        json=jsonable_encoder(group_update),
    )
    assert response.status_code == 404


@pytest.mark.anyio
async def test_set_student_to_group(
    client: AsyncClient, test_tutor, test_student, test_db_session
):
    _, token = await test_tutor()

    group_create = GroupCreate(name="Test Group")

    response = await client.post(
        "/group/create",
        headers={"Authorization": f"Bearer {token}"},
        json=jsonable_encoder(group_create),
    )
    group_id = response.json()["group_id"]

    student, token = await test_student()

    assert student.id

    set_student_to_group = SetStudentToGroup(student_id=student.id, group_id=group_id)

    response = await client.put(
        "/group/set_student",
        headers={"Authorization": f"Bearer {token}"},
        json=jsonable_encoder(set_student_to_group),
    )

    assert response.status_code == 204

    test_db_session.refresh(student)
    assert student.group_id == group_id


@pytest.mark.anyio
async def test_set_student_incorrect_student(
    client: AsyncClient,
    test_student,
    test_tutor,
):
    tutor, token = await test_tutor()

    group_create = GroupCreate(name="Test Group", tutor_id=tutor.id)

    response = await client.post(
        "/group/create",
        headers={"Authorization": f"Bearer {token}"},
        json=jsonable_encoder(group_create),
    )

    group_id = response.json()["group_id"]

    set_student_to_group = SetStudentToGroup(student_id=23123, group_id=group_id)

    response = await client.put(
        "/group/set_student",
        headers={"Authorization": f"Bearer {token}"},
        json=jsonable_encoder(set_student_to_group),
    )

    assert response.status_code == 400
