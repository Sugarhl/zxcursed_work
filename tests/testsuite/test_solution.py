import pytest

from httpx import AsyncClient
from server.storage.rocks_db_storage import RocksDBStorage
from server.utils import UserType
from server.models.lab_variant import LabVariant


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
    assert response.json()["solution_filename"] == "test_solution.ipynb"
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
    _, _, students, lab_variants = await test_vars_with_group()

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


@pytest.mark.anyio
async def test_get_solution(
    client: AsyncClient, test_vars_with_group, get_token, test_solution
):
    lab, _, students, lab_variants = await test_vars_with_group()

    lab_variant = lab_variants[0]
    token = get_token(students[0].id, UserType.STUDENT)

    solution = await test_solution(lab_variant)

    response = await client.get(
        f"/solution/get?solution_id={solution.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    response.json()["id"] == solution.id
    response.json()["file_key"] == solution.file_key


@pytest.mark.anyio
async def test_get_solution_invalid_solution_id(client: AsyncClient, test_student):
    _, token = test_student()
    response = await client.get(
        "/solution/get?solution_id=invalid_id",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_solution_by_tutor(
    client: AsyncClient, test_vars_with_group, get_token, test_solution
):
    _, tutor, _, lab_variants = await test_vars_with_group()
    lab_variant = lab_variants[0]

    solution = await test_solution(lab_variant)

    teacher_token = get_token(tutor.id, UserType.TUTOR)
    response = await client.get(
        f"/solution/get?solution_id={solution.id}",
        headers={"Authorization": f"Bearer {teacher_token}"},
    )
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_solution_unauthorized_lab_variant_access(
    client: AsyncClient, test_vars_with_group, get_token, test_solution
):
    _, _, students, lab_variants = await test_vars_with_group()
    lab_variant = lab_variants[0]
    token = get_token(students[0].id, UserType.STUDENT)

    solution = await test_solution(lab_variant)

    response = await client.get(
        f"/solution/get?solution_id={solution.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    unauthorized_token = get_token(students[1].id, UserType.STUDENT)
    response = await client.get(
        f"/solution/get?solution_id={solution.id}",
        headers={"Authorization": f"Bearer {unauthorized_token}"},
    )
    assert response.status_code == 403


@pytest.mark.anyio
async def test_get_solution_missing_solution_id(client: AsyncClient, test_student):
    _, token = test_student()
    response = await client.get(
        "/solution/get", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_mark_solution(
    client: AsyncClient, test_vars_with_group, get_token, test_solution, test_db_session
):
    _, tutor, _, lab_variants = await test_vars_with_group()

    lab_variant = lab_variants[0]
    token = get_token(tutor.id, UserType.TUTOR)

    solution = await test_solution(lab_variant)

    response = await client.post(
        "/solution/mark",
        json={"solution_id": solution.id, "mark": 9},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 202

    marked_solution = response.json()
    assert marked_solution["id"] == solution.id
    assert marked_solution["tutor_comment"] is None
    assert marked_solution["tutor_mark"] == 9

    response = await client.post(
        "/solution/mark",
        json={"solution_id": solution.id, "mark": 9, "comment": "comment"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 202

    marked_solution = response.json()
    assert marked_solution["id"] == solution.id
    assert marked_solution["tutor_comment"] == "comment"
    assert marked_solution["tutor_mark"] == 9
    assert marked_solution["lab_variant_id"] == lab_variant.id

    variant = test_db_session.get(LabVariant, lab_variant.id)
    assert variant.tutor_for_check_id == tutor.id


@pytest.mark.anyio
async def test_mark_solution_unauthorized_access(client: AsyncClient):
    response = await client.post("/solution/mark", json={"solution_id": 123, "mark": 9})
    assert response.status_code == 403


@pytest.mark.anyio
async def test_mark_solution_unauthorized_user_type(
    client: AsyncClient, test_vars_with_group, get_token, test_solution
):
    _, _, students, lab_variants = await test_vars_with_group()

    lab_variant = lab_variants[0]
    token = get_token(students[0].id, UserType.STUDENT)

    solution = await test_solution(lab_variant)
    response = await client.post(
        "/solution/mark",
        json={"solution_id": solution.id, "mark": 9},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


@pytest.mark.anyio
async def test_mark_solution_invalid_solution_id(client: AsyncClient, test_tutor):
    _, token = test_tutor()
    response = await client.post(
        "/solution/mark",
        json={"solution_id": "invalid_id", "mark": 9},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_mark_solution_invalid_mark(client: AsyncClient, test_tutor):
    _, token = test_tutor()
    response = await client.post(
        "/solution/mark",
        json={"solution_id": 456, "mark": "invalid_mark"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422
