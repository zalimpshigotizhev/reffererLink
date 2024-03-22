from typing import Any, Optional, List
from fastapi.exceptions import HTTPException

from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, UUID4


class UserBase(BaseModel):
    name: str
    surname: str
    email: EmailStr
    referral_code: Optional[str] = None


class UserSchemaRegister(UserBase):
    password: str

    @field_validator("password")
    def validate_password(cls, value: str) -> Any:
        if len(value) < 8:
            raise HTTPException(status_code=400,
                                detail="Password must be at least 8 characters long")
        return value


class UserSchema(UserBase):
    id: UUID4

    class Config:
        orm_mode = True


class UserList(BaseModel):
    users: List[UserSchema]


class UserSchemaLogin(BaseModel):
    email: EmailStr
    password: str



