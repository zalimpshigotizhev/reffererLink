from pydantic import BaseModel
from pydantic.types import UUID4
from typing import List, Optional, Annotated

from src.users.schemas import UserBase


class ReferralCodeSchema(BaseModel):
    id: UUID4
    code: str
    user_id: UserBase


class ReferralData(BaseModel):
    id: UUID4
    referral_code: Annotated[ReferralCodeSchema, str]
    referrer: UserBase
    referral: UserBase


class ReferralsList(BaseModel):
    referrals: List[ReferralData]
