from functools import wraps
import logging

from sqlalchemy.engine import Result
from sqlalchemy import Select

def one(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        query: Select = await func(self, *args, **kwargs)
        result: Result = await self.s.execute(query)

        return result.scalars().one_or_none()
    return wrapper

def all(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        query: Select = await func(self, *args, **kwargs)
        result: Result = await self.s.execute(query)

        value = result.scalars().all()
        
        return value
    return wrapper

def add(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        value = await func(self, *args, **kwargs)

        try:
            self.s.add(value)
            await self.s.commit()
        except Exception as e:
            logging.getLogger("DatabaseAdd").error("Ошибка: %s", e)

            await self.s.rollback()
    return wrapper