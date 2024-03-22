from sqlalchemy import select

from src.db.models import UserORM
from src.referralCode.models import ReferralCodeORM


async def pack_referrals(db, referrals: list):
    list_result = []
    for result in referrals:
        result_dict = {}
        result_dict["id"] = result.id
        user = await db.scalar(
            select(UserORM).where(UserORM.id == result.referral_id)
        )
        result_dict["referral"] = {
            "name": user.name,
            "surname": user.surname,
            "email": user.email,
        }
        code = await db.scalar(
            select(ReferralCodeORM).where(ReferralCodeORM.id == result.referral_code_id)
        )
        if code:
            referrer = await db.scalar(
                select(UserORM).where(UserORM.id == result.referrer_id)
            )
            result_dict["referral_code"] = {
                "id": code.id,
                "code": code.code,
                "user_id": {
                    "name": referrer.name,
                    "surname": referrer.surname,
                    "email": referrer.email,
                },
            }
        else:
            result_dict["referral_code"] = "К сожалению срок кода истек или владелец захотел его удалить!"
        list_result.append(result_dict)
    return list_result


    # dict_result = {
    #     "referrals": [
    #         {
    #             "id": result.id,
    #             "referral_id": {
    #                 "name": "Дамир",
    #                 "surname": "Варитлоов",
    #                 "email": "zalim@bk.ru",
    #             },
    #             "referral_code": {
    #                 "id": result.referral_code_id,
    #                 "code": "123456",
    #                 "user_id":  {
    #                             "name": "Залиим",
    #                             "surname": "Пшиготижев",
    #                             "email": "zalim@bk.ru",
    #                             },
    #             }
    #         }
    #     ]
    # }
