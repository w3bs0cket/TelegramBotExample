from typing import Dict

from aiogram.types import CallbackQuery

from ..annotations import Handler

class LogHandlers:
    def __init__(self):
        self.__handlers = {
            "delete": self._delete
        }

    async def _delete(self, call: CallbackQuery):
        try:
            await call.message.delete()
        except:
            pass

    async def handle(
        self,
        call: CallbackQuery
    ) -> None:
        action = call.data.split(":")[1]
        handler = self.__handlers.get(action)
        if not handler:
            return

        match action:
            case action:
                await handler(call)