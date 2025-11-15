from functools import wraps
from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def build(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        back_callback: Optional[str] = kwargs.pop("back_callback", None)
        cancel_callback: Optional[str] = kwargs.pop("cancel_callback", None)

        builder = InlineKeyboardBuilder()
        func(*args, b=builder, **kwargs)

        if back_callback:
            builder.row(
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=back_callback
                )
            )

        if cancel_callback:
            builder.row(
                InlineKeyboardButton(
                    text="❌ Отмена",
                    callback_data=cancel_callback
                )
            )

        return builder.as_markup()
    return wrapper