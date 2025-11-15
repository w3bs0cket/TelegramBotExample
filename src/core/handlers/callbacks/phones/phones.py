from typing import Dict

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from ....database.repositories.phones import PhoneRepos
from ..annotations import Handler
from ....keyboards import KeyboardFactory
from ...states.shemas import Phone as PhoneStates

class PhoneHandlers:
    def __init__(self):
        self.__handlers: Dict[str, Handler] = {
            "add": self._add
        }

    async def _add(
        self,
        call: CallbackQuery,
        state: FSMContext
    ) -> None:
        await state.set_state(PhoneStates.add_phone)

        msg = await call.message.edit_text(
            "📩 Отправьте номер телефона.\n📄 Можно списком, построчно.\n\nНапример:\n\n+7 (930) 000 00 00\n9304100000\n89304100000\n+7(930)4100000",
            reply_markup=KeyboardFactory.empty(cancel_callback="main_menu:menu")
        )

        await state.update_data({"message_id": msg.message_id})

    async def handle(
        self,
        call: CallbackQuery,
        state: FSMContext,
        phone_repo: PhoneRepos
    ) -> None:
        await state.clear()

        action = call.data.split(":")[1]
        handler = self.__handlers.get(action)

        match action:
            case "add":
                await handler(call,state)
