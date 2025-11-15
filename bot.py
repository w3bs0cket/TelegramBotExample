import asyncio
import logging
import os

from dotenv import load_dotenv

from aiogram import Dispatcher

from src.core.routers import build_user_router
from src.core import build_infra
from src.utils import init

async def main() -> None:
    await init()

    di = await build_infra()

    user_router = build_user_router(di)

    dp = Dispatcher()
    dp.include_router(user_router)

    await dp.start_polling(di.bot)

if __name__ == "__main__":
    load_dotenv()

    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s',
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    asyncio.run(main())