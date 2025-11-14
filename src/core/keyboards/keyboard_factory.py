from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .utils import build

class KeyboardFactory:
    @staticmethod
    def _btn(t: str, c: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=t, callback_data=c
        )

    @build
    def main_menu(b: InlineKeyboardBuilder) -> InlineKeyboardMarkup:
        b.row(
            KeyboardFactory._btn(
                "Настройки",
                "main_menu:settings"
            )
        )
        b.row(
            KeyboardFactory._btn(
                "Календарь",
                "main_menu:calendar"
            )
        )
        b.row(
            KeyboardFactory._btn(
                "Номера",
                "main_menu:phones"
            )
        )