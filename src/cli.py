import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram_dialog import setup_dialogs

from src.config import Settings
from src.db.factory import create_engine, create_session_factory
from src.dialogs import register_dialogs
from src.middlewares.db import DatabaseMiddleware
from src.middlewares.settings import SettingsMiddleware
from src.ui_commands import set_ui_commands

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    settings = Settings()

    engine = create_engine(connection_uri=settings.build_db_connection_uri())
    session_factory = create_session_factory(engine=engine)

    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN.get_secret_value())
    if settings.DEBUG:
        storage = MemoryStorage()
    else:
        storage = RedisStorage.from_url(
            url=settings.build_redis_connection_uri(),
            key_builder=DefaultKeyBuilder(with_destiny=True),
        )
    dp = Dispatcher(storage=storage)

    dp.update.outer_middleware(SettingsMiddleware(settings=settings))
    dp.update.outer_middleware(DatabaseMiddleware(session_factory=session_factory))

    register_dialogs(dp)
    setup_dialogs(dp)

    await set_ui_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        await engine.dispose()
        logger.info('Stopped')


if __name__ == "__main__":
    asyncio.run(main())
