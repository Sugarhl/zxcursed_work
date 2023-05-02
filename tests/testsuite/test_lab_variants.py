from httpx import AsyncClient
import pytest


from server.models.lab_variant import LabVariant
import server.schemas as schemas
from server.storage.rocks_db_storage import RocksDBStorage
from server.utils import UserType


pytestmark = pytest.mark.anyio


@pytest.mark.anyio
async def test_generate_variants_route(
    client: AsyncClient, test_lab_with_group, get_token
):
    lab, group, tutor, students = test_lab_with_group()

    token = get_token(tutor.id, UserType.TUTOR)

    # Generate variants for the group
    params = schemas.GenerateVariantsParams(
        lab_id=lab.id,
        group_id=group.id,
    )

    response = await client.post(
        "/variants/generate",
        headers={"Authorization": f"Bearer {token}"},
        json=params.dict(),
    )

    assert response.status_code == 201
    lab_variants = [LabVariant(**variant) for variant in response.json()]
    assert len(lab_variants) == len(students)

    storage = RocksDBStorage()
    for i, lab_variant in enumerate(lab_variants):
        assert lab_variant.lab_id == lab.id
        assert lab_variant.student_id == students[i].id
        assert lab_variant.variant_number == i
        assert lab_variant.variant_filename.endswith(".ipynb")
        assert lab_variant.file_key is not None
        assert await storage.get_file(lab_variant.file_key)


@pytest.mark.anyio
async def test_generate_variants_route_unauthorized(
    client: AsyncClient, test_lab_with_group
):
    lab, group, _, _ = test_lab_with_group()

    params = schemas.GenerateVariantsParams(
        lab_id=lab.id,
        group_id=group.id,
    )

    response = await client.post(
        "/variants/generate",
        json=params.dict(),
    )

    assert response.status_code == 401


@pytest.mark.anyio
async def test_generate_variants_route_wrong_user_type(
    client: AsyncClient, test_lab_with_group, get_token
):
    lab, group, student, _ = test_lab_with_group()

    token = get_token(student.id, UserType.STUDENT)

    params = schemas.GenerateVariantsParams(
        lab_id=lab.id,
        group_id=group.id,
    )

    response = await client.post(
        "/variants/generate",
        headers={"Authorization": f"Bearer {token}"},
        json=params.dict(),
    )

    assert response.status_code == 403


@pytest.mark.anyio
async def test_generate_variants_route_invalid_lab_id(
    client: AsyncClient, test_lab_with_group, get_token
):
    lab, _, tutor, _ = test_lab_with_group()

    token = get_token(tutor.id, UserType.TUTOR)

    params = schemas.GenerateVariantsParams(
        lab_id=999,
        group_id=1,
    )

    response = await client.post(
        "/variants/generate",
        headers={"Authorization": f"Bearer {token}"},
        json=params.dict(),
    )

    assert response.status_code == 404


@pytest.mark.anyio
async def test_generate_variants_route_invalid_group_id(
    client: AsyncClient, test_lab_with_group, get_token
):
    lab, _, tutor, _ = test_lab_with_group()

    token = get_token(tutor.id, UserType.TUTOR)

    params = schemas.GenerateVariantsParams(
        lab_id=lab.id,
        group_id=999,
    )

    response = await client.post(
        "/variants/generate",
        headers={"Authorization": f"Bearer {token}"},
        json=params.dict(),
    )

    assert response.status_code == 404
