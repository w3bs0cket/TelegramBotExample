from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
)

class Database:
    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = None

    async def connect(self) -> None:
        if self._engine is None:
            self._engine = create_async_engine(self._dsn)
            self._sessionmaker = async_sessionmaker(self._engine, expire_on_commit=False)

    async def disconnect(self) -> None:
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._sessionmaker = None

    @property
    def sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        assert self._sessionmaker is not None, "Call connect() first"
        return self._sessionmaker
    
    @asynccontextmanager
    async def session(self):
        async with self.sessionmaker() as s:
            yield s