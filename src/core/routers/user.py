from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.filters.command import CommandStart

from ..di import Container
from ..middlewares import RepositoriesMiddleware, KeyboardsMiddleware
from ..handlers.messages import CommandsHandler
from ..handlers.callbacks import MenuHandlers, PhoneHandlers, DayHandlers
from ..handlers.states import PhoneFsmHnalders
from ..keyboards import KeyboardFactory
from ..handlers.states.shemas import Phone as PhoneStateGroup

def build(di: Container) -> Router:
    r = Router(name="Users")

    r.message.middleware(KeyboardsMiddleware(keyboard_factory=KeyboardFactory))
    r.message.middleware(RepositoriesMiddleware(di.db))

    r.message.register(CommandsHandler.start, CommandStart())

    phone_fsm_handlers = PhoneFsmHnalders()
    r.message.register(phone_fsm_handlers.handle, StateFilter(PhoneStateGroup))

    r.callback_query.middleware(KeyboardsMiddleware(keyboard_factory=KeyboardFactory))
    r.callback_query.middleware(RepositoriesMiddleware(di.db))

    menu_handlers = MenuHandlers()
    phone_handlers = PhoneHandlers()
    day_handlers = DayHandlers()

    r.callback_query.register(menu_handlers.handle, F.data.startswith("main_menu:"))
    r.callback_query.register(phone_handlers.handle, F.data.startswith("phones:"))
    r.callback_query.register(day_handlers.handle, F.data.startswith("days:"))

    return r