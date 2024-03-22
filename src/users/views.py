from fastapi import (
    APIRouter, Depends, HTTPException,
)
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.config import get_db
from src.db.models import UserORM
from src.referralCode.models import ReferralCodeORM, ReferrerReferralORM
from src.users.schemas import UserSchemaRegister, UserSchemaLogin, UserBase, UserList
from src.utils import hash_password, validate_password, encode_jwt, decode_jwt, http_bearer

router = APIRouter(prefix="/users", tags=["AUTH"])


@router.post("/register/")
async def register(
    db: AsyncSession = Depends(get_db),
    user_data: UserSchemaRegister = Depends(),
) -> UserBase:
    new_user = UserORM(
        name=user_data.name,
        surname=user_data.surname,
        email=user_data.email,
        password=hash_password(user_data.password),
        referral_code=user_data.referral_code,
    )
    db.add(new_user)
    await db.flush()

    if new_user.referral_code:
        ref_code_obj = await db.scalar(select(ReferralCodeORM).where(ReferralCodeORM.code == new_user.referral_code))

        if not ref_code_obj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Referral code not found",
            )

        new_refferal = ReferrerReferralORM(
            referrer_id=ref_code_obj.user_id,
            referral_id=new_user.id,
            referral_code_id=ref_code_obj.id
        )

        db.add(new_refferal)

    await db.commit()
    await db.refresh(new_user)

    return UserBase(
        name=new_user.name,
        surname=new_user.surname,
        email=new_user.email,
        referral_code=new_user.referral_code
    )


@router.get("/login/")
async def login(
    db: AsyncSession = Depends(get_db),
    user_data: UserSchemaLogin = Depends(),
):
    user = await db.scalar(select(UserORM).where(UserORM.email == user_data.email))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not validate_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    data = {
        "sub": str(user.id),
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
    }
    token = encode_jwt(data)
    return token


@router.get("/users/me/")
async def check_info_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    token = credentials.credentials
    data = decode_jwt(token=token)
    return data
