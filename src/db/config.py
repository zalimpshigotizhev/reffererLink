import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base


engine = create_async_engine(
    "postgresql+asyncpg://postgres:552216742@localhost:5432/postgres",
    echo=True,
)


new_session = sessionmaker(bind=engine, expire_on_commit=False)


async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(create_tables(engine))



