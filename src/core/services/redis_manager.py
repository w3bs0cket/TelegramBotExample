import asyncio
import logging

from typing import Awaitable, Callable

from redis.asyncio import Redis

class RedisManager:
    def __init__(
        self,
        url: str
    ) -> None:
        self.redis = Redis

        self._url = url
        self._logger = logging.getLogger("RedisManager")
        self._listener_task: asyncio.Task | None = None

        self._message_handler: Callable[[str], Awaitable[None]] = None

    async def _connect(self):
        self.redis = Redis.from_url(self._url, decode_responses=True)
        await self.redis.ping()
        self._logger.info("Редис подключен.")

    async def _close(self):
        self._running = False
        if self._listener_task:
            self._listener_task.cancel()
        if self.redis:
            await self.redis.close()
        logging.info("Редис закрыт.")

    async def _listener(self):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(*["log"])
        self._logger.info("Редис подписался на каналы.")

        async for msg in pubsub.listen():
            if msg["type"] == "message":
                channel = msg["channel"]
                data = msg["data"]

                if channel == "log":
                    await self._message_handler(data)

    async def send(self, channel: str, message: str):
        if not self.redis:
            raise RuntimeError("Редис не подключен.")
        
        await self.redis.publish(channel, message)

    def subscribe_handler(self, handler: Callable[[str], Awaitable[None]]):
        self._message_handler = handler

    async def start_listening(self):
        if not self.redis:
            raise RuntimeError("Редис не подключен.")
        if self._listener_task:
            raise RuntimeError("Редис уже слушает каналы.")
        self._running = True
        self._listener_task = asyncio.create_task(self._listener())