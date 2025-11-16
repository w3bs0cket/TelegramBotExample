from typing import Dict

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from ....database.repositories.days import DayRepos
from ....database.tables.tables import DaySettings
from ....keyboards import KeyboardFactory
from ..annotations import Handler

class DayHandlers:
    def __init__(self):
        self.__handlers: Dict[str, Handler] = {
            "activate": self._activate,
            "day": self._day,
            "hint": self._hint,
            "start": self._start,
            "end": self._end
        }

    async def __day_menu(self, call: CallbackQuery, day: DaySettings, text_base: str = None) -> None:
        if not text_base:
            text_base = "🏷️ <b>{}</b>\n\n▶️ Начало: <code>{}:00</code>\n⏹️ Конец: <code>{}:00</code>"

        await call.message.edit_text(
            text_base.format(
                KeyboardFactory.days_names[day.day_number], day.start_hour, day.end_hour
            ),
            reply_markup=KeyboardFactory.day_menu(day=day, back_callback="main_menu:calendar")
        )

    async def _hint(self, call: CallbackQuery) -> None:
        await call.answer("💡 Используйте стрелочки чтобы изменить время.")

    async def _start(self, call: CallbackQuery, repo: DayRepos, day_index: int, new_value: int) -> None:
        day = await repo.update_start_time(day_index, new_value)

        await self.__day_menu(call, day, text_base="🏷️ <b>{}</b>\n\n> ▶️ Начало: <code>{}:00</code>\n⏹️ Конец: <code>{}:00</code>")

    async def _end(self, call: CallbackQuery, repo: DayRepos, day_index: int, new_value: int) -> None:
        day = await repo.update_end_time(day_index, new_value)

        await self.__day_menu(call, day, text_base="🏷️ <b>{}</b>\n\n▶️ Начало: <code>{}:00</code>\n> ⏹️ Конец: <code>{}:00</code>")

    async def _activate(self, call: CallbackQuery, repo: DayRepos, day_index: int) -> None:
        day = await repo.reverse_active_status(day_index)

        await self.__day_menu(call, day)

    async def _day(self, call: CallbackQuery, repo: DayRepos, day_index: int) -> None:
        day = await repo.get_day(day_index)
        if not day:
            await call.answer("День не найден.")
            return

        await self.__day_menu(call, day)

    async def handle(
        self,
        call: CallbackQuery,
        state: FSMContext,
        day_repo: DayRepos
    ) -> None:
        await call.answer()
        await state.clear()

        call_data = call.data.split(":")

        handler = self.__handlers.get(call_data[1])
        if not handler:
            return

        match call_data:
            case [_, "activate", i, *__]:
                await handler(call, day_repo, int(i))
            case [_, "day", i, *__]:
                await handler(call, day_repo, int(i))
            case [_, "hint", *__]:
                await handler(call)
            case [_, "start", i, value, *__]:
                await handler(call, day_repo, int(i), int(value))
            case [_, "end", i, value, *__]:
                await handler(call, day_repo, int(i), int(value))