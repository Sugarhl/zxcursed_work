import pytest

from httpx import AsyncClient
from server.storage.rocks_db_storage import RocksDBStorage
from server.utils import UserType


pytestmark = pytest.mark.anyio


@pytest.mark.anyio
async def test_upload_solution(client: AsyncClient, test_vars_with_group, get_token):
    lab, _, students, lab_variants = await test_vars_with_group()

    lab_variant = lab_variants[0]
    token = get_token(students[0].id, UserType.STUDENT)

    solution_data = {
        "lab_variant_id": lab_variant.id,
        "comment": "Test solution comment",
    }

    filename = "test_solution.ipynb"
    file_data = b"test solution contents"

    files = {"file": (filename, file_data)}

    response = await client.post(
        "/solution/upload_solution",
        headers={"Authorization": f"Bearer {token}"},
        data=solution_data,
        files=files,
    )

    assert response.status_code == 201
    assert response.json()["filename"] == "test_solution.ipynb"
    assert response.json()["lab_variant_id"] == lab_variant.id

    file_key = response.json()["file_key"]
    assert file_key is not None
    storage = RocksDBStorage()
    file_content = await storage.get_file(file_key)
    assert file_data == file_content


@pytest.mark.anyio
async def test_upload_solution_student_access(
    client: AsyncClient, test_vars_with_group, get_token
):
    lab, group, students, lab_variants = await test_vars_with_group()

    student_1 = students[0]
    lab_variant = lab_variants[0]

    assert student_1.id == lab_variant.student_id
    student_2 = students[1]
    assert student_2.id != lab_variant.student_id

    payload = {
        "lab_variant_id": lab_variant.id,
        "comment": "Test solution comment",
    }

    files = {"file": ("test_solution.ipynb", b"test solution contents")}

    token = get_token(student_2.id, UserType.STUDENT)
    response = await client.post(
        "/solution/upload_solution",
        headers={"Authorization": f"Bearer {token}"},
        data=payload,
        files=files,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "User does not have access to lab variant"


@pytest.mark.anyio
async def test_upload_solution_access_error(
    client: AsyncClient, test_vars_with_group, get_token
):
    _, _, students, lab_variants = await test_vars_with_group()
    _, _, _, other_group_variants = await test_vars_with_group()

    other_group_variant = other_group_variants[0]

    token = get_token(students[0].id, UserType.STUDENT)

    solution_data = {
        "lab_variant_id": other_group_variant.id,
        "comment": "Test solution comment",
    }

    filename = "test_solution.ipynb"
    file_data = b"test solution contents"

    files = {"file": (filename, file_data)}

    response = await client.post(
        "/solution/upload_solution",
        headers={"Authorization": f"Bearer {token}"},
        data=solution_data,
        files=files,
    )

    assert response.status_code == 403
    assert "User does not have access to lab variant" in response.json()["detail"]


async def test_upload_solution_route_invalid_lab_variant_id(
    client: AsyncClient, test_vars_with_group, get_token
):
    _, _, students, _ = await test_vars_with_group()

    token = get_token(students[0].id, UserType.STUDENT)

    solution_data = {
        "lab_variant_id": 9999,
        "comment": "Test solution comment",
    }

    filename = "test_solution.ipynb"
    file_data = b"test solution contents"

    files = {"file": (filename, file_data)}

    response = await client.post(
        "/solution/upload_solution",
        headers={"Authorization": f"Bearer {token}"},
        data=solution_data,
        files=files,
    )

    assert response.status_code == 404


async def test_upload_solution_unsupported_file_type(
    client: AsyncClient, test_vars_with_group, get_token
):
    lab, _, students, lab_variants = await test_vars_with_group()

    lab_variant = lab_variants[0]
    token = get_token(students[0].id, UserType.STUDENT)

    solution_data = {
        "lab_variant_id": lab_variant.id,
        "comment": "Test solution comment",
    }

    filename = "test_solution.pdf"
    file_data = b"test solution contents"

    files = {"file": (filename, file_data)}

    response = await client.post(
        "/solution/upload_solution",
        headers={"Authorization": f"Bearer {token}"},
        data=solution_data,
        files=files,
    )

    assert response.status_code == 422


async def test_upload_solution_missing_file(
    client: AsyncClient, test_vars_with_group, get_token
):
    lab, _, students, lab_variants = await test_vars_with_group()

    lab_variant = lab_variants[0]
    token = get_token(students[0].id, UserType.STUDENT)

    solution_data = {
        "lab_variant_id": lab_variant.id,
        "comment": "Test solution comment",
    }

    response = await client.post(
        "/solution/upload_solution",
        headers={"Authorization": f"Bearer {token}"},
        data=solution_data,
    )

    assert response.status_code == 422
