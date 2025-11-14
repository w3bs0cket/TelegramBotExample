from typing import Callable, Awaitable

from aiogram.types import CallbackQuery

Handler=Callable[[CallbackQuery], Awaitable[None]]