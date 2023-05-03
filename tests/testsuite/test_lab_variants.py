from httpx import AsyncClient
import pytest


from server.models.lab_variant import LabVariant
import server.schemas as schemas
from server.storage.rocks_db_storage import RocksDBStorage
from server.utils import UserType


pytestmark = pytest.mark.anyio


@pytest.mark.anyio
async def test_generate_variants(client: AsyncClient, test_lab_with_group, get_token):
    lab, group, tutor, students = test_lab_with_group()

    token = get_token(tutor.id, UserType.TUTOR)

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
async def test_generate_variants_empty_group(
    client: AsyncClient, test_lab_with_empty_group, get_token
):
    lab, group, tutor = test_lab_with_empty_group()
    token = get_token(tutor.id, UserType.TUTOR)

    params = schemas.GenerateVariantsParams(
        lab_id=lab.id,
        group_id=group.id,
    )

    response = await client.post(
        "/variants/generate",
        headers={"Authorization": f"Bearer {token}"},
        json=params.dict(),
    )

    assert response.status_code == 400


@pytest.mark.anyio
async def test_generate_variants_unauthorized(client: AsyncClient, test_lab_with_group):
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
async def test_generate_variants_wrong_user_type(
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
async def test_generate_variants_invalid_lab_id(
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
async def test_generate_variants_invalid_group_id(
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


@pytest.mark.anyio
async def test_get_student_variants(
    client: AsyncClient, test_vars_with_group, get_token
):
    lab, _, students, _ = await test_vars_with_group()

    for student in students:
        student_token = get_token(student.id, UserType.STUDENT)

        response = await client.post(
            "/variants/student/all",
            headers={"Authorization": f"Bearer {student_token}"},
        )

        assert response.status_code == 201
        student_lab_variants = [LabVariant(**variant) for variant in response.json()]
        assert len(student_lab_variants) == 1

        student_lab_variant = student_lab_variants[0]
        assert student_lab_variant.lab_id == lab.id
        assert student_lab_variant.student_id == student.id
        assert student_lab_variant.variant_filename.endswith(".ipynb")
        assert student_lab_variant.file_key is not None
        assert await RocksDBStorage().get_file(student_lab_variant.file_key)


@pytest.mark.anyio
async def test_get_student_variants_not_allow(
    client: AsyncClient, test_vars_with_group, get_token
):
    _, tutor, students, _ = await test_vars_with_group()

    token = get_token(tutor.id, UserType.TUTOR)

    response = await client.post(
        "/variants/student/all",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403

    student_token = get_token(students[0].id, UserType.STUDENT)

    response = await client.post(
        "/variants/student/all",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert response.status_code == 201
    student_lab_variants = [LabVariant(**variant) for variant in response.json()]
    assert len(student_lab_variants) == 1


@pytest.mark.anyio
async def test_get_student_var_by_id(
    client: AsyncClient, test_vars_with_group, get_token
):
    _, _, students, lab_variants = await test_vars_with_group()
    student = students[0]

    variant = lab_variants[0]

    student_token = get_token(student.id, UserType.STUDENT)
    response = await client.post(
        f"/variants/student/{variant.id}",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert response.status_code == 201

    student_lab_variant = LabVariant(**response.json())
    assert student_lab_variant.file_key == variant.file_key
    assert student_lab_variant.variant_filename == variant.variant_filename
    assert student_lab_variant.lab_id == variant.lab_id
    assert student_lab_variant.student_id == variant.student_id


@pytest.mark.anyio
async def test_get_student_var_by_id_not_allow(
    client: AsyncClient, test_vars_with_group, get_token
):
    _, tutor, students, lab_variants = await test_vars_with_group()

    tutor_token = get_token(tutor.id, UserType.TUTOR)
    student_token = get_token(students[0].id, UserType.STUDENT)
    student_token_1 = get_token(students[1].id, UserType.STUDENT)

    response = await client.post(
        f"/variants/student/{lab_variants[0].id}",
        headers={"Authorization": f"Bearer {tutor_token}"},
    )
    assert response.status_code == 403

    response = await client.post(
        f"/variants/student/{lab_variants[1].id}",
        headers={"Authorization": f"Bearer {student_token}"},
    )

    assert response.status_code == 403

    response = await client.post(
        f"/variants/student/{lab_variants[0].id}",
        headers={"Authorization": f"Bearer {student_token_1}"},
    )

    assert response.status_code == 403

    _, _, _, other_lab_variants = await test_vars_with_group()

    response = await client.post(
        f"/variants/student/{other_lab_variants[0].id}",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert response.status_code == 403


@pytest.mark.anyio
async def test_get_variants_by_student_id(
    client: AsyncClient, test_vars_with_group, get_token
):
    lab, tutor, students, _ = await test_vars_with_group()
    token = get_token(tutor.id, UserType.TUTOR)

    for student in students:
        response = await client.post(
            f"/variants/tutor/all-by-student/{student.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        print(response.json())
        assert response.status_code == 201
        student_lab_variants = [LabVariant(**variant) for variant in response.json()]
        assert len(student_lab_variants) == 1

        student_lab_variant = student_lab_variants[0]
        assert student_lab_variant.lab_id == lab.id
        assert student_lab_variant.student_id == student.id
        assert student_lab_variant.variant_filename.endswith(".ipynb")
        assert student_lab_variant.file_key is not None
        assert await RocksDBStorage().get_file(student_lab_variant.file_key)


@pytest.mark.anyio
async def test_get_variants_by_student_id_negative(
    client: AsyncClient, test_vars_with_group, get_token
):
    _, tutor, students, _ = await test_vars_with_group()

    student_token = get_token(students[0].id, UserType.STUDENT)
    tutor_token = get_token(tutor.id, UserType.TUTOR)

    response = await client.post(
        f"/variants/tutor/all-by-student/{students[0].id}",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert response.status_code == 403

    response = await client.post(
        f"/variants/tutor/all-by-student/{999}",
        headers={"Authorization": f"Bearer {tutor_token}"},
    )
    assert response.status_code == 404


@pytest.mark.anyio
async def test_get_var_by_id(client: AsyncClient, test_vars_with_group, get_token):
    _, tutor, students, lab_variants = await test_vars_with_group()

    variant = lab_variants[0]

    tutor_token = get_token(tutor.id, UserType.TUTOR)

    response = await client.post(
        f"/variants/tutor/variant/{variant.id}",
        headers={"Authorization": f"Bearer {tutor_token}"},
    )
    assert response.status_code == 201

    student_lab_variant = LabVariant(**response.json())
    assert student_lab_variant.file_key == variant.file_key
    assert student_lab_variant.variant_filename == variant.variant_filename
    assert student_lab_variant.lab_id == variant.lab_id
    assert student_lab_variant.student_id == variant.student_id

    token = get_token(students[0].id, UserType.STUDENT)
    response = await client.post(
        f"/variants/tutor/variant/{variant.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403
