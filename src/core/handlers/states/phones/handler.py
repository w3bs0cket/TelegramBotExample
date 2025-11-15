import logging
import re
from typing import Dict
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ....database.repositories.phones import PhoneRepos
from ....keyboards import KeyboardFactory
from ...callbacks.annotations import Handler

class PhoneFsmHnalders:
    def __init__(self):
        self.__handlers: Dict[str, Handler] = {
            "add_phone": self._add
        }

        self._logger = logging.getLogger("PhoneFsmHandler")

    async def __delete_msg(self, msg: Message, target: int) -> None:
        try:
            await msg.bot.delete_message(chat_id=msg.chat.id, message_id=target)
        except:
           pass

    def __normalize_phone(self, phone: str) -> str:
        digits = re.sub(r"\D", "", phone)
        
        if not digits:
            return None

        if digits.startswith("8") and len(digits) == 11:
            digits = "7" + digits[1:]
        elif digits.startswith("7") and len(digits) == 11:
            pass
        elif digits.startswith("9") and len(digits) == 10:
            digits = "7" + digits
        else:
            return None

        if len(digits) != 11 or not digits.startswith("7"):
            return None

        return f"+{digits}"

    async def _add(
        self,
        msg: Message, 
        state: FSMContext, 
        phone_repo: PhoneRepos
    ) -> None:
        if not msg.text:
            await msg.answer(
                "Не правильный формат.",
                reply_markup=KeyboardFactory.empty(cancel_callback="main_menu:phones:1")
            )
            return
        
        phones_to_add = []

        if "\n" in msg.text:
            phones_to_add = msg.text.split("\n")
        else:
            phones_to_add.append(msg.text.strip())

        await state.clear()

        good = 0
        for phone_to_add in phones_to_add:
            phone = self.__normalize_phone(phone_to_add)
            if not phone:
                continue

            exists = await phone_repo.get_phone(phone=phone)
            if exists:
                continue

            try:
                await phone_repo.add(phone)

                good += 1
            except Exception as e:
                self._logger.error("Ошибка добавления номера: %s | %s", e, phone)

        await msg.answer(
            "💡 Добавлено: <code>{}</code> из <code>{}</code>".format(good, len(phones_to_add)),
            reply_markup=KeyboardFactory.empty(back_callback="main_menu:phones:1")
        )

    async def handle(
        self,
        message: Message,
        state: FSMContext,
        phone_repo: PhoneRepos
    ) -> None:
        current = await state.get_state()
        _, action = current.split(":")

        handler = self.__handlers.get(action)
        if not handler:
            return
        
        data = await state.get_data()

        msg_to_delete = int(data.get("message_id", -1))
        if msg_to_delete:
            await self.__delete_msg(message, msg_to_delete)
        
        match action:
            case "add_phone":
                await handler(message, state, phone_repo)