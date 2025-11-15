from datetime import datetime
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...tables.tables import Phones
from ..utils import one, all, add

class PhoneRepos:
    def __init__(self, session: AsyncSession):
        self.s = session

    @all
    async def get_phones_page(self, page: int = 1, limit: int = 9) -> List[Phones]:
        offset = (page - 1) * limit

        return select(Phones).offset(offset).limit(limit)
    
    @add
    async def add(self, phone: str) -> None:
        return Phones(phone=phone)
    
    @one
    async def get_phone(self, i: int = None, phone: str = None) -> Optional[Phones]:
        if not i and not phone:
            raise RuntimeError("В метод должен быть хотя бы передан один из аргументов.")
        
        if i:
            return select(Phones).where(Phones.id == i)
        elif phone:
            return select(Phones).where(Phones.phone == phone)