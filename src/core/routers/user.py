from aiogram import Router, F
from aiogram.filters.command import CommandStart

from ..di import Container
from ..middlewares import RepositoriesMiddleware, KeyboardsMiddleware
from ..handlers.messages import CommandsHandler
from ..handlers.callbacks import MenuHandlers
from ..keyboards import KeyboardFactory

def build(di: Container) -> Router:
    r = Router(name="Users")

    r.message.middleware(KeyboardsMiddleware(keyboard_factory=KeyboardFactory))
    r.message.middleware(RepositoriesMiddleware(di.db))

    r.message.register(CommandsHandler.start, CommandStart())

    r.callback_query.middleware(KeyboardsMiddleware(keyboard_factory=KeyboardFactory))
    r.callback_query.middleware(RepositoriesMiddleware(di.db))

    menu_handler = MenuHandlers()

    r.callback_query.register(menu_handler.handle, F.data.startswith("main_menu:"))

    return r