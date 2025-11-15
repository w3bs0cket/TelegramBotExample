from datetime import datetime
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...tables.tables import DaySettings
from ..utils import one, all

class DayRepos:
    def __init__(self, session: AsyncSession):
        self.s = session

    @property
    def day_index(self) -> int:
        return datetime.weekday() + 1

    @one
    async def get_day(self, day_index: int = None) -> Optional[DaySettings]:
        i = self.day_index if day_index is None else day_index
        return select(DaySettings).where(
            DaySettings.day_number == i
        )
    
    @all
    async def get_days(self) -> List[DaySettings]:
        return select(DaySettings)