from aiogram import BaseMiddleware
        
class KeyboardsMiddleware(BaseMiddleware):
    def __init__(self, keyboard_factory: ...):
        self.kb = keyboard_factory

    async def __call__(self, handler, event, data):
        data["keyboard"] = self.kb
        return await handler(event, data)