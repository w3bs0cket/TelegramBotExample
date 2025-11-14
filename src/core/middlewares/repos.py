from aiogram import BaseMiddleware

from ..database.repositories.days import DayRepos
from ..database import Database
        
class RepositoriesMiddleware(BaseMiddleware):
    def __init__(self, db: Database):
        self._db = db

    async def __call__(self, handler, event, data):
        async with self._db.session() as s:
            data["day_repo"] = DayRepos(s)
            return await handler(event, data)