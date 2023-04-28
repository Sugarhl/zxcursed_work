from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from server.database import get_db
from server.token import auth_by_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
bearer = HTTPBearer()


@router.post("/protected", status_code=status.HTTP_200_OK)
async def upload_solution(
    auth: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    user, _ = await auth_by_token(db=db, token=auth.credentials)
    return {
        "authorized": True,
        "message": f"Welcome {user.first_name} {user.last_name}!!",
    }
