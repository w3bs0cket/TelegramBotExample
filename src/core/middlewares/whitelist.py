from aiogram import BaseMiddleware

class WhiteListMiddleware(BaseMiddleware):
    def __init__(self, admin: int):
        self._whitelisted = set()

        self._whitelisted.add(int(admin)) # can be change to list in the future. but i need just one admin.

    async def __call__(self, handler, event, data):
        user = data.get("event_from_user", None)
        if user is None:
            return await handler(event, data)
        
        if user.id in self._whitelisted:
            return await handler(event, data)