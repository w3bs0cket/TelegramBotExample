from typing import Dict

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from ....database.repositories.settings import SettingRepos
from ....database.tables.tables import Settings
from ....keyboards import KeyboardFactory
from ..annotations import Handler

class SettingHandlers:
    def __init__(self):
        self.__handlers: Dict[str, Handler] = {
            "delay": self._delay,
            "offset": self._offset
        }

    async def __upd_menu(self, call: CallbackQuery, settings: Settings, text_base: str = None) -> None:
        if not text_base:
            text_base = "⚙️ <b>Настройки</b>\n\n⌛ Задержка поднятий: <code>{}</code>\n💤 Разброс: <code>{}</code>"
        
        await call.message.edit_text(
            text_base.format(
                settings.up_delay, settings.up_offset
            ),
            reply_markup=KeyboardFactory.settings_menu(back_callback="main_menu:menu", settings=settings)
        )

    async def _delay(self, call: CallbackQuery, repo: SettingRepos, value: int) -> None:
        settings = await repo.change_delay(value)

        try:
            await self.__upd_menu(call, settings, "⚙️ <b>Настройки</b>\n\n> ⌛ Задержка поднятий: <code>{}</code>\n💤 Разброс: <code>{}</code>")
        except:
            await call.answer()

    async def _offset(self, call: CallbackQuery, repo: SettingRepos, value: int) -> None:
        settings = await repo.change_offset(value)

        try:
            await self.__upd_menu(call, settings, "⚙️ <b>Настройки</b>\n\n⌛ Задержка поднятий: <code>{}</code>\n> 💤 Разброс: <code>{}</code>")
        except:
            await call.answer()

    async def handle(
        self,
        call: CallbackQuery,
        state: FSMContext,
        setting_repo: SettingRepos
    ) -> None:
        await state.clear()

        call_data = call.data.split(":")

        handler = self.__handlers.get(call_data[1])
        if not handler:
            await call.answer()
            return
        
        match call_data:
            case [_, "delay", value, *__]:
                await handler(call, setting_repo, int(value))
            case [_, "offset", value, *__]:
                await handler(call, setting_repo, int(value))