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
            "add": self._add,
            "remove": self._remove,
            "phone": self._phone
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

    async def _phone(
        self,
        call: CallbackQuery,
        repo: PhoneRepos
    ) -> None:
        phone_id = call.data.split(":")[-1]

        phone = await repo.get_phone(i=int(phone_id))
        if not phone:
            await call.answer("Запись не найдена.")
            return

        await call.message.edit_text(
            text="📞 Номер: <code>{}</code>\n\nПоднимался в текущем цикле: <b>{}</b>".format(phone.phone, "Да" if phone.viewed else "Нет"),
            reply_markup=KeyboardFactory.phone(phone_id=phone_id, back_callback="main_menu:phones:1")
        )

    async def _remove(
        self,
        call: CallbackQuery,
        repo: PhoneRepos
    ) -> None:
        phone_id = call.data.split(":")[-1]

        await repo.remove(int(phone_id))

        await call.message.edit_text(
            text="✅ Номер удален.",
            reply_markup=KeyboardFactory.empty(back_callback="main_menu:phones:1")
        )

    async def handle(
        self,
        call: CallbackQuery,
        state: FSMContext,
        phone_repo: PhoneRepos
    ) -> None:
        await state.clear()

        action = call.data.split(":")[1]
        handler = self.__handlers.get(action)
        if not handler:
            await call.answer()
            return

        match action:
            case "add":
                await handler(call,state)
            case "remove":
                await handler(call, phone_repo)
            case "phone":
                await handler(call, phone_repo)