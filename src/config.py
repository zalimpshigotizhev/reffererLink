from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "src" / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "src" / "certs" / "public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 60


class DB(BaseModel):
    user: str = "postgres"
    password: str = "552216742"
    host: str = "localhost"
    port: int = 5432
    database: str = "postgres"


class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()
    db: DB = DB()


settings = Settings()
