from aiogram.types import Message

from ...keyboards import KeyboardFactory

class CommandsHandler:
    @staticmethod
    async def start(msg: Message, keyboard: KeyboardFactory) -> None:
        await msg.answer(
            "🛠️ <b>Панель управления</b>", 
            reply_markup=keyboard.main_menu()
        )