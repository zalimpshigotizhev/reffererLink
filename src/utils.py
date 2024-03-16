import jwt
from core.config import settings

def encode_jwt(
    data: dict,
    key: str,
    algorithm: str,
) -> str:
    return jwt.encode(data, key, algorithm=algorithm)


def decode_jwt(
    token: str,
    key: str,
    algorithms: str,
) -> dict:
    return jwt.decode(token, key, algorithms=[algorithms])


