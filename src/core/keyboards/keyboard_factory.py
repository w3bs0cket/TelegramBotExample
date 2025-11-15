from typing import ClassVar, List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .utils import build
from ..database.tables.tables import DaySettings, Phones

class KeyboardFactory:
    days_names: ClassVar[dict[int, str]] = {
        1: "Понедельник",
        2: "Вторник",
        3: "Среда",
        4: "Четверг",
        5: "Пятница",
        6: "Суббота",
        7: "Воскресенье",
    }

    @classmethod
    def day_name(cls, i: int) -> str:
        return cls.days_names[i]

    @staticmethod
    def _btn(t: str, c: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=t, callback_data=c
        )

    @build
    def empty(b: InlineKeyboardBuilder) -> InlineKeyboardMarkup:
        pass

    @build
    def main_menu(b: InlineKeyboardBuilder) -> InlineKeyboardMarkup:
        b.row(
            KeyboardFactory._btn(
                "⚙️ Настройки",
                "main_menu:settings"
            )
        )
        b.row(
            KeyboardFactory._btn(
                "📅 Календарь",
                "main_menu:calendar"
            )
        )
        b.row(
            KeyboardFactory._btn(
                "📞 Номера",
                "main_menu:phones:1"
            )
        )

    @build
    def settings_menu(b: InlineKeyboardBuilder) -> InlineKeyboardMarkup:
        b.row(
            KeyboardFactory._btn(
                "Задержка поднятий",
                "settings_menu:up_delay"
            )
        )
        b.row(
            KeyboardFactory._btn(
                "Разброс",
                "settings_menu:offset"
            )
        )

    @build
    def calendar_menu(days: List[DaySettings], b: InlineKeyboardBuilder) -> InlineKeyboardMarkup:
        for day in days:
            emoji = "🟢" if day.active else "⚪"
            text = f"{emoji} {KeyboardFactory.day_name(day.day_number)}"
            callback_data = "days:day:{}".format(day.day_number)

            btn = KeyboardFactory._btn(text, callback_data)

            if day.day_number in {1, 3, 5, 7}:
                b.row(btn)
            else:
                b.add(btn)

    @build
    def phone(phone_id: int, b: InlineKeyboardBuilder) -> InlineKeyboardMarkup:
        b.row(
            KeyboardFactory._btn(
                "🗑️ Удалить",
                f"phones:remove:{phone_id}"
            )
        )

    @build
    def phones_page(phones: List[Phones], page: int, b: InlineKeyboardBuilder) -> InlineKeyboardMarkup:
        for i, phone in enumerate(phones):
            btn = KeyboardFactory._btn(phone.phone, "phones:phone:{}".format(phone.id))

            if i==0 or i%3 == 0:
                b.row(btn)
            else:
                b.add(btn)

        b.row(
            KeyboardFactory._btn(
                "➕ Добавить",
                "phones:add"
            )
        )

        b.row(
            KeyboardFactory._btn(
                "<-",
                "main_menu:phones:{}".format(int(page)-1)
            )
        )
        b.add(
            KeyboardFactory._btn(
                "->",
                "main_menu:phones:{}".format(int(page)+1)
            )
        )

    @build
    def day_menu(day: DaySettings, b: InlineKeyboardBuilder) -> InlineKeyboardMarkup:
        b.row(
            KeyboardFactory._btn(
                "🟢" if day.active is False else "⚪",
                "days:activate:{}".format(day.day_number)
            )
        )