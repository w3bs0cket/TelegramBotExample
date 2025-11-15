import os

from dotenv import load_dotenv

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from ..core.database.tables.base import BaseModel
from ..core.database.tables.tables import DaySettings

async def seed_days(async_session_maker: async_sessionmaker[AsyncSession]) -> None:
    async with async_session_maker() as session:
        count = await session.scalar(
            select(func.count()).select_from(DaySettings)
        )

        if not count:
            session.add_all(
                [DaySettings(day_number=i) for i in range(1, 8)]
            )
            await session.commit()

async def init() -> None:
    db_url = os.getenv("DATABASE")
    if not db_url:
        raise RuntimeError("Env var DATABASE не задана")

    engine = create_async_engine(db_url, echo=False)

    async_session_maker = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    await seed_days(async_session_maker)

    await engine.dispose()
