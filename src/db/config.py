import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.config import settings
from .models import Base
from src.config import settings



engine = create_async_engine(
    settings.db_url,
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


