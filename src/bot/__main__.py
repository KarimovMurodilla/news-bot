"""This file represent startup bot logic."""
import asyncio
import logging

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from redis.asyncio.client import Redis

from src.cache import Cache
from src.configuration import conf
from src.db.database import create_async_engine
from src.language.translator import Translator
from src.bot.dispatcher import get_dispatcher, get_redis_storage
from src.bot.structures.data_structure import TransferData

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from src.scheduler.tasks import parse_and_save_db


async def start_bot():
    """This function will start bot with polling mode."""
    bot = Bot(token=conf.bot.token, default=DefaultBotProperties(parse_mode='html'))
    cache = Cache()
    storage = get_redis_storage(
        redis=Redis(
            db=conf.redis.db,
            host=conf.redis.host,
            password=conf.redis.passwd,
            username=conf.redis.username,
            port=conf.redis.port,
        )
    )
    dp = get_dispatcher(storage=storage)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(parse_and_save_db, IntervalTrigger(minutes=2))
    scheduler.start()

    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        **TransferData(
            engine=create_async_engine(url=conf.db.build_connection_str()),
            cache=cache
        ),
        translator=Translator(),
    )


if __name__ == '__main__':
    logging.basicConfig(level=conf.logging_level)
    asyncio.run(start_bot())
