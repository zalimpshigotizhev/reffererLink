from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "src" / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "src" / "certs" / "public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 60


class DB(BaseModel):
    DB_NAME: str = os.environ.get("DB_NAME", "postgres")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "aa")
    DB_USER: str = os.environ.get("DB_USER", "postgres")
    DB_HOST: str = os.environ.get("DB_HOST", "localhost")
    DB_PORT: int = os.environ.get("DB_PORT", 5432)


class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()
    db: DB = DB()
    db_url: str = f"postgresql+asyncpg://{db.DB_USER}:{db.DB_PASSWORD}@{db.DB_HOST}:{db.DB_PORT}/{db.DB_NAME}"


settings = Settings()
