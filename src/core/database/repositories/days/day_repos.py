from datetime import datetime
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from ...tables.tables import DaySettings
from ..utils import one, all, upd

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
        return select(DaySettings).order_by(DaySettings.day_number)
    
    @upd
    async def reverse_active_status(self, day_index: int) -> DaySettings:
        return update(DaySettings).where(DaySettings.day_number == day_index).values(active=~DaySettings.active).returning(DaySettings)
    
    @upd
    async def update_start_time(self, day_index: int, new_value: int) -> DaySettings:
        return update(DaySettings).where(DaySettings.day_number == day_index).values(start_hour=new_value).returning(DaySettings)
    
    @upd
    async def update_end_time(self, day_index: int, new_value: int) -> DaySettings:
        return update(DaySettings).where(DaySettings.day_number == day_index).values(end_hour=new_value).returning(DaySettings)