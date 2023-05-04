from httpx import AsyncClient
import pytest

from server.storage.rocks_db_storage import RocksDBStorage
from server.utils import UserType


pytestmark = pytest.mark.anyio


@pytest.mark.anyio
async def test_get_lab_variant_file(
    client: AsyncClient, test_vars_with_group, get_token
):
    _, _, students, lab_variants = await test_vars_with_group()

    student = students[0]
    lab_variant = lab_variants[0]

    file_key = lab_variant.file_key
    file_name = lab_variant.variant_filename
    file_contents = b"Test file contents"
    await RocksDBStorage().update_file(file_key, file_contents)

    token = get_token(student.id, UserType.STUDENT)
    response = await client.get(
        "/file/get/variant",
        params={"file_key": file_key, "file_name": file_name},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    assert (
        response.headers["content-disposition"]
        == f'attachment; filename="{lab_variant.variant_filename}"'
    )
    assert await response.aread() == file_contents


@pytest.mark.anyio
async def test_get_lab_variant_file_file_not_found(
    client: AsyncClient, test_vars_with_group, get_token
):
    _, _, students, lab_variants = await test_vars_with_group()

    student = students[0]
    lab_variant = lab_variants[0]

    file_key = "random_key"
    file_name = lab_variant.variant_filename

    token = get_token(student.id, UserType.STUDENT)
    response = await client.get(
        "/file/get/variant",
        params={"file_key": file_key, "file_name": file_name},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


@pytest.mark.anyio
async def test_get_lab_variant_file_missing_file_key(
    client: AsyncClient, test_vars_with_group, get_token
):
    _, _, students, lab_variants = await test_vars_with_group()

    student = students[0]
    lab_variant = lab_variants[0]

    file_name = lab_variant.variant_filename

    token = get_token(student.id, UserType.STUDENT)
    response = await client.get(
        "/file/get/variant",
        params={"file_name": file_name},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_lab_variant_file_missing_file_name(
    client: AsyncClient, test_vars_with_group, get_token
):
    _, _, students, lab_variants = await test_vars_with_group()

    student = students[0]
    lab_variant = lab_variants[0]

    file_key = lab_variant.file_key

    token = get_token(student.id, UserType.STUDENT)
    response = await client.get(
        "/file/get/variant",
        params={"file_key": file_key},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_solution_file(
    client: AsyncClient, test_vars_with_group, get_token, test_solution
):
    _, _, students, lab_variants = await test_vars_with_group()

    student = students[0]
    lab_variant = lab_variants[0]
    solution = await test_solution(lab_variant)

    file_key = solution.file_key
    file_name = solution.solution_filename
    file_contents = b"Test file contents"
    await RocksDBStorage().update_file(file_key, file_contents)

    token = get_token(student.id, UserType.STUDENT)
    response = await client.get(
        "/file/get/solution",
        params={"file_key": file_key, "file_name": file_name},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    assert (
        response.headers["content-disposition"]
        == f'attachment; filename="{solution.solution_filename}"'
    )
    assert await response.aread() == file_contents


@pytest.mark.anyio
async def test_get_solution_file_by_tutor(
    client: AsyncClient, test_vars_with_group, get_token, test_solution
):
    _, tutor, students, lab_variants = await test_vars_with_group()

    lab_variant = lab_variants[0]
    solution = await test_solution(lab_variant)

    file_key = solution.file_key
    file_name = solution.solution_filename
    file_contents = b"Test file contents"
    await RocksDBStorage().update_file(file_key, file_contents)

    token = get_token(tutor.id, UserType.TUTOR)
    response = await client.get(
        "/file/get/solution",
        params={"file_key": file_key, "file_name": file_name},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    assert (
        response.headers["content-disposition"]
        == f'attachment; filename="{solution.solution_filename}"'
    )
    assert await response.aread() == file_contents


@pytest.mark.anyio
async def test_get_solution_file_by_other_student(
    client: AsyncClient, test_vars_with_group, get_token, test_solution
):
    _, _, students, lab_variants = await test_vars_with_group()

    lab_variant = lab_variants[0]
    solution = await test_solution(lab_variant)

    file_key = solution.file_key
    file_name = solution.solution_filename
    file_contents = b"Test file contents"
    await RocksDBStorage().update_file(file_key, file_contents)

    student = students[2]
    token = get_token(student.id, UserType.STUDENT)
    response = await client.get(
        "/file/get/solution",
        params={"file_key": file_key, "file_name": file_name},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403


@pytest.mark.anyio
async def test_get_solution_file_file_not_found(
    client: AsyncClient, test_vars_with_group, get_token, test_solution
):
    _, _, students, lab_variants = await test_vars_with_group()

    student = students[0]
    lab_variant = lab_variants[0]
    solution = await test_solution(lab_variant)

    file_key = "random_key"
    file_name = solution.solution_filename

    token = get_token(student.id, UserType.STUDENT)
    response = await client.get(
        "/file/get/solution",
        params={"file_key": file_key, "file_name": file_name},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


@pytest.mark.anyio
async def test_get_solution_file_missing_file_key(
    client: AsyncClient, test_vars_with_group, get_token, test_solution
):
    _, _, students, lab_variants = await test_vars_with_group()

    student = students[0]
    lab_variant = lab_variants[0]
    solution = await test_solution(lab_variant)

    file_name = solution.solution_filename

    token = get_token(student.id, UserType.STUDENT)
    response = await client.get(
        "/file/get/solution",
        params={"file_name": file_name},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_solution_file_missing_file_name(
    client: AsyncClient, test_vars_with_group, get_token, test_solution
):
    _, _, students, lab_variants = await test_vars_with_group()

    student = students[0]
    lab_variant = lab_variants[0]
    solution = await test_solution(lab_variant)

    file_key = solution.file_key

    token = get_token(student.id, UserType.STUDENT)
    response = await client.get(
        "/file/get/solution",
        params={"file_key": file_key},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422
