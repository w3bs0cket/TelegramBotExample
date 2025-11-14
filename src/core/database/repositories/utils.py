from functools import wraps

from sqlalchemy.engine import Result
from sqlalchemy import Select

def one(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        query: Select = await func(self, *args, **kwargs)
        result: Result = await self.s.execute(query)

        value = result.scalars().one_or_none()
        if value is None:
            raise RuntimeError(f"Record not found for query: {query}")
        
        return value
    return wrapper

def all(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        query: Select = await func(self, *args, **kwargs)
        result: Result = await self.s.execute(query)

        value = result.scalars().all()
        
        return value
    return wrapper