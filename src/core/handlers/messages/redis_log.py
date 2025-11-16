import os

from aiogram import Bot

from ...keyboards import KeyboardFactory

class RedisLogHandler:
    def __init__(
        self,
        bot: Bot
    ) -> None:
        self._bot = bot

    async def handler(self, msg: str) -> None:
        await self._bot.send_message(
            chat_id=os.getenv("ADMIN_ID"),
            text=f"✏️ <b>[Лог]</b>: {msg}",
            reply_markup=KeyboardFactory.log_ok()
        )