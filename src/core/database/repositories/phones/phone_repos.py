from datetime import datetime
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...tables.tables import Phones
from ..utils import one, all

class PhoneRepos:
    def __init__(self, session: AsyncSession):
        self.s = session

    @all
    async def get_phones_page(self, page: int = 1, limit: int = 9) -> List[Phones]:
        offset = (page - 1) * limit

        return select(Phones).offset(offset).limit(limit)