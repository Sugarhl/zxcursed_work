import io

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession


from server.CRUD.lab_variant import get_lab_variant_by_file_key_checked
from server.database import get_db
from server.storage.rocks_db_storage import RocksDBStorage
from server.token import auth_by_token


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
