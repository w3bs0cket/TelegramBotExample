from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...tables.tables import DaySettings
from ..utils import execute_scalar_one

class DayRepos:
    def __init__(self, session: AsyncSession):
        self.s = session

    @property
    def day_index(self) -> int:
        return datetime.weekday() + 1

    @execute_scalar_one
    async def get_day(self) -> Optional[DaySettings]:
        return select(DaySettings).where(
            DaySettings.day_number == self.day_index
        )