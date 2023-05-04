import io

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession


from server.CRUD.lab_variant import (
    get_lab_variant_by_file_key_checked,
    get_lab_variant_checked,
)
from server.CRUD.solution import get_lab_solution_by_file_key_checked
from server.database import get_db
from server.storage.rocks_db_storage import RocksDBStorage
from server.token import auth_by_token
from server.utils import UserType
from server.validation.checks import lab_var_check_access


router = APIRouter()
bearer = HTTPBearer(auto_error=False)


@router.get("/get/variant", response_class=StreamingResponse)
async def get_lab_variant_file(
    file_key: str,
    file_name: str,
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    await auth_by_token(db=db, auth=auth)

    await get_lab_variant_by_file_key_checked(db=db, file_key=file_key)

    file_storage = RocksDBStorage()
    file = await file_storage.get_file_checked(file_key)

    return StreamingResponse(
        io.BytesIO(file),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
    )


@router.get("/get/solution", response_class=StreamingResponse)
async def get_solution_file(
    file_key: str,
    file_name: str,
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    user, user_type = await auth_by_token(db=db, auth=auth)

    solution = await get_lab_solution_by_file_key_checked(db=db, file_key=file_key)

    variant = await get_lab_variant_checked(
        db=db, lab_variant_id=solution.lab_variant_id
    )

    if user_type == UserType.STUDENT:
        lab_var_check_access(lab_variant=variant, student=user)

    file_storage = RocksDBStorage()
    file = await file_storage.get_file_checked(file_key)

    return StreamingResponse(
        io.BytesIO(file),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
    )
