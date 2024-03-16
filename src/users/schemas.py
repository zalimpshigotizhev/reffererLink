from pydantic import BaseModel
from pydantic import EmailStr


class UserSchema(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    password: str


