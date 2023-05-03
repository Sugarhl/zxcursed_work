from argparse import FileType
import io
from typing import List


from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession


import server.schemas as schemas

from server.CRUD.group import get_group_checked
from server.CRUD.lab import get_lab_checked
from server.CRUD.lab_variant import (
    create_lab_variant_from_dict,
    get_all_lab_variants_by_student_id,
    get_lab_variant,
    get_lab_variant_by_file_key_checked,
    get_lab_variant_checked,
)
from server.CRUD.student import get_student_checked, get_students_by_group

from server.generation.base import Variant
from server.generation.generate import generate_for_group

from server.models.lab import Lab
from server.models.lab_variant import LabVariant
from server.models.student import Student

from server.database import get_db
from server.storage.rocks_db_storage import RocksDBStorage
from server.token import auth_by_token
from server.validation.checks import student_access_check, tutor_access_check

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
