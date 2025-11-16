import os

from dataclasses import dataclass

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from .database import Database
from .services import RedisManager

@dataclass(frozen=True)
class Settings:
    bot_token: str = os.getenv("BOT_TOKEN")
    db_dsn: str = os.getenv("DATABASE")
    redis: str = os.getenv("REDIS")

@dataclass(frozen=True)
class Container:
    settings: Settings
    bot: Bot
    db: Database
    redis: RedisManager

async def build_infra() -> Container:
    settings = Settings()

    db = Database(dsn=settings.db_dsn)
    await db.connect()

    redis = RedisManager(settings.redis)
    await redis._connect()
    await redis.start_listening()

    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode="html"))
    
    return Container(
        settings=settings,
        bot=bot,
        db=db,
        redis=redis
    )