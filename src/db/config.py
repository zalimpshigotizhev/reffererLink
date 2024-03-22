import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.config import settings
from .models import Base

DB_NAME = settings.db.database
DB_PASSWORD = settings.db.password
DB_USER = settings.db.user
DB_HOST = settings.db.host
DB_PORT = settings.db.port


engine = create_async_engine(
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    echo=True,
)


new_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    await create_tables(engine)
    db = new_session()
    try:
        yield db
    finally:
        await db.close()


