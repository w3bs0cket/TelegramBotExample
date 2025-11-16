from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from ...tables.tables import Settings
from ..utils import one, upd

class SettingRepos:
    def __init__(self, session: AsyncSession):
        self.s = session

    @one
    async def get_settings(self) -> Settings:
        return select(Settings).where(Settings.id == 1)
    
    @upd
    async def change_delay(self, new_value: int) -> Settings:
        return update(Settings).where(Settings.id == 1).values(up_delay=new_value).returning(Settings)
    
    @upd
    async def change_offset(self, new_value: int) -> Settings:
        return update(Settings).where(Settings.id == 1).values(up_offset=new_value).returning(Settings)