from typing import Dict

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from ....database.repositories.days import DayRepos
from ....database.repositories.phones import PhoneRepos
from ....keyboards import KeyboardFactory
from ..annotations import Handler

class MenuHandlers:
    def __init__(self):
        self.__handlers: Dict[str, Handler] = {
            "menu": self._menu,
            "settings": self._settings_menu,
            "calendar": self._calendar_menu,
            "phones": self._phones_menu
        }

    async def _menu(self, call: CallbackQuery) -> None:
        await call.message.edit_text(
            text="🛠️ <b>Панель управления</b>",
            reply_markup=KeyboardFactory.main_menu()
        )

    async def _settings_menu(self, call: CallbackQuery) -> None:
        await call.message.edit_text(
            text="⚙️ <b>Настройки</b>",
            reply_markup=KeyboardFactory.settings_menu(back_callback="main_menu:menu")
        )

    async def _calendar_menu(self, call: CallbackQuery, repo: DayRepos) -> None:
        days = await repo.get_days()
        if not days:
            await call.answer("Календарь пуст.")
            return

        await call.message.edit_text(
            text="🗓️ <b>Календарь поднятий</b>",
            reply_markup=KeyboardFactory.calendar_menu(days=days, back_callback="main_menu:menu")
        )

    async def _phones_menu(self, call: CallbackQuery, repo: PhoneRepos) -> None:
        page = int(call.data.split(":")[-1])

        if page < 1:
            await call.answer("⚠️ Вы на первой странице.")
            return
        
        phones = await repo.get_phones_page(page)

        if page > 1 and len(phones) < 1:
            await call.answer("⚠️ Вы на последней странице.")
            return

        epoch_value = 0
        for phone in phones:
            if phone.viewed:
                epoch_value += 1

        await call.message.edit_text(
            text="📞 <b>Номера для поднятий</b>\n\nВсего: <code>{}</code>\nТекущий круг: <code>{}</code>".format(len(phones), epoch_value),
            reply_markup=KeyboardFactory.phones_page(phones=phones, page=page, back_callback="main_menu:menu")
        )

    async def handle(
        self, 
        call: CallbackQuery, 
        state: FSMContext,
        day_repo: DayRepos,
        phone_repo: PhoneRepos
    ) -> None:
        await state.clear()

        action = call.data.split(":")[1]
        handler = self.__handlers.get(action)

        if not handler:
            return
        
        match action:
            case "menu":
                await handler(call)
            case "calendar":
                await handler(call, day_repo)
            case "settings":
                await handler(call)
            case "phones":
                await handler(call, phone_repo)

