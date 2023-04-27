from server.schemas import GroupCreate, GroupUpdate
from httpx import AsyncClient
import pytest
from server.models.group import Group

from server.schemas import GroupCreate
from fastapi.encoders import jsonable_encoder

pytestmark = pytest.mark.anyio


@pytest.mark.anyio
async def test_create_group(client: AsyncClient, test_tutor, test_db_session):
    tutor, token, creds = test_tutor

    group_create = GroupCreate(
        name="Test Group",
        tutor_id=creds.user_id
    )

    response = await client.post("/group/create", headers={"Authorization": f"Bearer {token}"},
                                 json=jsonable_encoder(group_create))

    assert response.status_code == 201

    # Check that the group was created in the database
    group_id = response.json()["group_id"]
    group_db = test_db_session.get(Group, group_id)
    assert group_db.id == group_id
    assert group_db.name == group_create.name
    assert group_db.tutor_id == creds.user_id


@pytest.mark.anyio
async def test_create_group_negative(client: AsyncClient, test_student, test_tutor):

    _, token, _ = test_student

    group_create = GroupCreate(
        name="Test Group",
    )

    response = await client.post("/group/create", headers={"Authorization": f"Bearer {token}"},
                                 json=jsonable_encoder(group_create))

    assert response.status_code == 403


@pytest.mark.anyio
async def test_get_group(client: AsyncClient, test_tutor):
    tutor, token, creds = test_tutor

    group_create = GroupCreate(
        name="Test Group",
        tutor_id=creds.user_id
    )

    response = await client.post("/group/create", headers={"Authorization": f"Bearer {token}"},
                                 json=jsonable_encoder(group_create))
    group_id = response.json()["group_id"]

    response = await client.get(f"/group/get/{group_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["id"] == group_id
    assert response.json()["name"] == group_create.name
    assert response.json()["tutor_id"] == creds.user_id


@pytest.mark.anyio
async def test_get_group_negative(client: AsyncClient, test_student):
    _, token, _ = test_student

    response = await client.get(f"/group/get/{100}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404


@pytest.mark.anyio
async def test_update_group_name(client: AsyncClient, test_tutor, test_db_session):
    tutor, token, creds = test_tutor

    group_create = GroupCreate(
        name="Test Group"
    )

    response = await client.post("/group/create", headers={"Authorization": f"Bearer {token}"},
                                 json=jsonable_encoder(group_create))
    group_id = response.json()["group_id"]

    group_update = GroupUpdate(
        name="Updated Test Group"
    )

    response = await client.put(f"/group/update/{group_id}", headers={"Authorization": f"Bearer {token}"},
                                json=jsonable_encoder(group_update))

    assert response.status_code == 204

    group_db = test_db_session.get(Group, group_id)
    assert group_db.id == group_id
    assert group_db.name == group_update.name


@pytest.mark.anyio
async def test_update_group_tutor(client: AsyncClient, test_tutor, test_db_session):
    tutor, token, creds = test_tutor
    _, _, new_tutor_creds = test_tutor

    group_create = GroupCreate(
        name="Test Group"
    )

    response = await client.post("/group/create", headers={"Authorization": f"Bearer {token}"},
                                 json=jsonable_encoder(group_create))
    group_id = response.json()["group_id"]

    group_update = GroupUpdate(
        name="Updated Test Group",
        tutor_id=new_tutor_creds.user_id
    )

    response = await client.put(f"/group/update/{group_id}", headers={"Authorization": f"Bearer {token}"},
                                json=jsonable_encoder(group_update))

    assert response.status_code == 204

    group_db = test_db_session.get(Group, group_id)
    assert group_db.id == group_id
    assert group_db.name == group_update.name
    assert group_db.tutor_id == group_update.tutor_id


@pytest.mark.anyio
async def test_update_group_negative(client: AsyncClient, test_student, test_tutor):

    tutor, token, creds = test_tutor

    group_create = GroupCreate(
        name="Test Group"
    )

    response = await client.post("/group/create", headers={"Authorization": f"Bearer {token}"},
                                 json=jsonable_encoder(group_create))

    group_id = response.json()["group_id"]

    _, token, _ = test_student

    group_update = GroupUpdate(
        name="Updated Test Group",
    )

    response = await client.put(f"/group/update/{group_id}", headers={"Authorization": f"Bearer {token}"},
                                json=jsonable_encoder(group_update))
    assert response.status_code == 403

    tutor, token, creds = test_tutor

    response = await client.put(f"/group/update/{1000000}", headers={"Authorization": f"Bearer {token}"},
                                json=jsonable_encoder(group_update))
    assert response.status_code == 404
