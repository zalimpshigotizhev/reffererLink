import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from sqlalchemy.future import select
from src.db.config import get_db
from src.referralCode.utils import pack_referrals
from src.utils import is_autenticated, decode_jwt, check_code_activate
from src.referralCode.models import ReferralCodeORM, ReferrerReferralORM

router = APIRouter(prefix="/referral", tags=["REFERRAL-CODE"])


# Функция для получения всех кодов пользователя
async def get_all_codes(db: AsyncSession, user_id: str):
    return await db.scalar(
        select(ReferralCodeORM).where(ReferralCodeORM.user_id == user_id)
    )


@router.post("/code/create/")
async def create_code(
    code: str,
    minutes: int,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(is_autenticated),
):
    data = decode_jwt(token)

    aviability_obj = await db.scalar(
        select(ReferralCodeORM).where(ReferralCodeORM.user_id == data["sub"])
    )

    if aviability_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="У вас уже есть активный код для рефералов.",
        )

    now = datetime.datetime.now(datetime.UTC)

    if minutes:
        life_time = now + datetime.timedelta(minutes=minutes)
    else:
        life_time = now + datetime.timedelta(minutes=minutes)

    new_code = ReferralCodeORM(code=code, user_id=data["sub"], life_time=life_time.timestamp())
    db.add(new_code)
    await db.commit()
    await db.refresh(new_code)
    return new_code


@router.delete("/code/delete/")
async def delete_code(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(is_autenticated),
):
    data = decode_jwt(token)

    current_code = await db.scalar(
        select(ReferralCodeORM).where(ReferralCodeORM.user_id == data["sub"])
    )
    if not current_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="У вас нет активного кода для рефералов.",
        )

    await db.delete(current_code)
    await db.commit()
    return {
        "message": "Код для рефералов был удален.",
    }


@router.get("/code/my/")
async def get_my_code(
    token: str = Depends(is_autenticated),
    db: AsyncSession = Depends(get_db),
):
    data = decode_jwt(token)

    code_obj = await get_all_codes(db, data["sub"])

    if code_obj:
        await check_code_activate(db, code_obj)
    else:
        return "У вас нет активного кода для рефералов."
    return code_obj


@router.get("/codes/{user_id}/")
async def get_code_by_id(
    id: str,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(is_autenticated),
):
    referrals_by_user_id = await db.scalars(
        select(ReferrerReferralORM).where(ReferrerReferralORM.referrer_id == id)
    )
    results = referrals_by_user_id.all()

    list_result = await pack_referrals(db, results)

    return {"referrals": list_result}



