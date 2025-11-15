from typing import Dict

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from ....database.repositories.days import DayRepos
from ....keyboards import KeyboardFactory
from ..annotations import Handler

class DayHandlers:
    def __init__(self):
        self.__handlers: Dict[str, Handler] = {
            "activate": self._activate,
            "day": self._day
        }

    async def _activate(self, call: CallbackQuery, repo: DayRepos, day_index: int) -> None:
        day = await repo.reverse_active_status(day_index)

        await call.message.edit_reply_markup(
            reply_markup=KeyboardFactory.day_menu(day=day, back_callback="main_menu:calendar")
        )

    async def _day(self, call: CallbackQuery, repo: DayRepos, day_index: int) -> None:
        day = await repo.get_day(day_index)
        if not day:
            await call.answer("День не найден.")
            return

        await call.message.edit_text(
            "🏷️ <b>{}</b>\n\n▶️ Начало: <code>{}:00</code>\n⏹️ Конец: <code>{}:00</code>".format(
                KeyboardFactory.days_names[day_index], day.start_hour, day.end_hour
            ),
            reply_markup=KeyboardFactory.day_menu(day=day, back_callback="main_menu:calendar")
        )

    async def handle(
        self,
        call: CallbackQuery,
        state: FSMContext,
        day_repo: DayRepos
    ) -> None:
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