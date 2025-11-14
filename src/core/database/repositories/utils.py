from functools import wraps
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

def execute_scalar_one(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        query: Select = func(self, *args, **kwargs)
        result = await self.s.execute(query)

        value = result.scalars().one_or_none()
        if value is None:
            raise RuntimeError(f"Record not found for query: {query}")
        
        return value
    return wrapper