import os

from aiogram.filters.command import CommandStart
from aiogram.filters import StateFilter
from aiogram import Router, F

from ..middlewares import RepositoriesMiddleware, RedisMiddleware, WhiteListMiddleware
from ..handlers.states.shemas import Phone as PhoneStateGroup
from ..handlers.messages import CommandsHandler, RedisLogHandler
from ..handlers.states import PhoneFsmHnalders
from ..handlers.callbacks import (
    MenuHandlers, PhoneHandlers, 
    DayHandlers, SettingHandlers,
    LogHandlers
)
from ..di import Container

def build(di: Container) -> Router:
    r = Router(name="Users")

    di.redis.subscribe_handler(RedisLogHandler(di.bot).handler)

    # r.message.middleware(WhiteListMiddleware(admin=os.getenv("ADMIN_ID")))
    # r.callback_query.middleware(WhiteListMiddleware(admin=os.getenv("ADMIN_ID")))

    r.message.middleware(RedisMiddleware(redis=di.redis))
    r.message.middleware(RepositoriesMiddleware(di.db))

    r.message.register(CommandsHandler.start, CommandStart())
    r.message.register(PhoneFsmHnalders().handle, StateFilter(PhoneStateGroup))

    r.callback_query.middleware(RedisMiddleware(redis=di.redis))
    r.callback_query.middleware(RepositoriesMiddleware(di.db))

    r.callback_query.register(MenuHandlers().handle, F.data.startswith("main_menu:"))
    r.callback_query.register(PhoneHandlers().handle, F.data.startswith("phones:"))
    r.callback_query.register(DayHandlers().handle, F.data.startswith("days:"))
    r.callback_query.register(SettingHandlers().handle, F.data.startswith("settings:"))
    r.callback_query.register(LogHandlers().handle, F.data.startswith("log:"))

    return r