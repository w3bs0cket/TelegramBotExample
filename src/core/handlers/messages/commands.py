from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ...keyboards import KeyboardFactory

class CommandsHandler:
    @staticmethod
    async def start(msg: Message, state: FSMContext) -> None:
        await state.clear()

        await msg.answer(
            "🛠️ <b>Панель управления</b>", 
            reply_markup=KeyboardFactory.main_menu()
        )