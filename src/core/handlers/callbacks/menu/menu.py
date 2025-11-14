from typing import Dict

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from ....keyboards import KeyboardFactory
from ..annotations import Handler

class MenuHandlers:
    def __init__(self):
        self.__handlers: Dict[str, Handler] = {
            "menu": self._menu,
            "settings": self._settings_menu,
            "calendar": self._calendar_menu
        }

    async def _menu(self, call: CallbackQuery) -> None:
        await call.message.edit_text(
            text="🛠️ <b>Панель управления</b>",
            reply_markup=KeyboardFactory.main_menu()
        )

    async def _settings_menu(self, call: CallbackQuery) -> None:
        await call.message.edit_text(
            text="⚙️ <b>Настройки</b>",
            reply_markup=KeyboardFactory.settings_menu()
        )

    async def _calendar_menu(self, call: CallbackQuery) -> None:
        await call.message.edit_text(
            text="🗓️ <b>Календарь поднятий</b>",
            reply_markup=KeyboardFactory.calendar_manu()
        )

    async def _phones_menu(self, call: CallbackQuery) -> None:
        await call.message.edit_text(
            text="📞 <b>Номера для поднятий</b>",
            reply_markup=KeyboardFactory.phones_page()
        )

    async def handle(
        self, 
        call: CallbackQuery, 
        state: FSMContext
    ) -> None:
        await state.clear()

        action = call.data.split(":")[1]
        handler = self.__handlers.get(action)

        if not handler:
            return
        
        match action:
            case "menu":
                await handler(call)

