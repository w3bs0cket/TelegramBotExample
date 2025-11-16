from aiogram import BaseMiddleware

from ..database.repositories.days import DayRepos
from ..database.repositories.phones import PhoneRepos
from ..database.repositories.settings import SettingRepos
from ..database import Database
        
class RepositoriesMiddleware(BaseMiddleware):
    def __init__(self, db: Database):
        self._db = db

    async def __call__(self, handler, event, data):
        async with self._db.session() as s:
            data["day_repo"] = DayRepos(s)
            data["phone_repo"] = PhoneRepos(s)
            data["setting_repo"] = SettingRepos(s)
            return await handler(event, data)