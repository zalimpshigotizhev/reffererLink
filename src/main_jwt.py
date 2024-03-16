from fastapi import APIRouter
from users.schemas import UserSchema

zalim = UserSchema(
    id=1,
    name="zalim",
    surname="pshigotizhev",
    email="zalim@mail.ru",
    password="1231231"
)

islam = UserSchema(
    id=2,
    name="islam",
    surname="pshigotizhev",
    email="islam@mail.ru",
    password="1231231"
)


users: dict[str, UserSchema] = {
    zalim.name: zalim,
    islam.name: islam
}



router = APIRouter(prefix='/jwt', tags=['auth'])


