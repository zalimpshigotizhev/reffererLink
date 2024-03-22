import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.config import settings
from typing import Union
from datetime import timedelta
import datetime
import bcrypt

from src.db.config import get_db
from src.referralCode.models import ReferralCodeORM

http_bearer = HTTPBearer()

oauth2 = OAuth2PasswordBearer(
    tokenUrl="/users/login/"
)

def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: Union[timedelta, None] = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.datetime.now(datetime.UTC)

    if expire_timedelta:
        expire_minutes = now + expire_timedelta
    else:
        expire_minutes = now + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire_minutes, "iat": now})

    return jwt.encode(to_encode, private_key, algorithm=algorithm)


def decode_jwt(
    token: Union[str, bytes],
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    return jwt.decode(token, public_key, algorithms=[algorithm])


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode('utf-8')
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    pwd_bytes: bytes = password.encode()
    return bcrypt.checkpw(pwd_bytes, hashed_password)


def is_autenticated(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
):
    credentials = credentials.credentials
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials


async def check_code_activate(
    db: AsyncSession,
    code_obj: ReferralCodeORM,
):
    now = datetime.datetime.now(datetime.UTC).timestamp()

    if now > code_obj.life_time:
        code = await db.scalar(
            select(ReferralCodeORM).where(ReferralCodeORM.id == code_obj.id)
        )
        await db.delete(code)
        await db.commit()

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="У кода вышел срок действия !",
        )

