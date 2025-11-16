from aiogram import BaseMiddleware

from ..services import RedisManager

class RedisMiddleware(BaseMiddleware):
    def __init__(self, redis: RedisManager):
        self.redis = redis

    async def __call__(self, handler, event, data):
        data["redis"] = self.redis
        return await handler(event, data)