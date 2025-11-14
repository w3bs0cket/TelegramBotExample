from functools import wraps
from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def build(func, back_callback: Optional[str] = None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        builder = InlineKeyboardBuilder()
        func(*args, b=builder, **kwargs)

        if back_callback:
            builder.row(
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=back_callback
                )
            )
            
        return builder.as_markup()
    return wrapper