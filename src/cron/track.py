import asyncio
import logging
from datetime import UTC, datetime

from aiogram import Bot, Dispatcher
from aiogram.fsm.state import State
from aiogram_dialog import StartMode, setup_dialogs
from aiogram_dialog.api.protocols import BgManagerFactory

from src.config import Settings
from src.db.factory import create_engine, create_session_factory
from src.db.provider import DatabaseProvider
from src.dialogs import register_dialogs
from src.factory import create_bot, create_storage
from src.middlewares.db import DatabaseMiddleware
from src.middlewares.settings import SettingsMiddleware
from src.states import TrackSG

logger = logging.getLogger(__name__)

SLEEP_TIME = 2 * 60


class ControllerNotificator:
    def __init__(
        self,
        bot: Bot,
        manager_factory: BgManagerFactory,
        provider: DatabaseProvider,
        track_state: State,
    ) -> None:
        self.manage_factory = manager_factory
        self.provider = provider
        self.track_state = track_state
        self.bot = bot

    async def send_notifications(self) -> None:
        now = datetime.now(tz=UTC)
        users = await self.provider.user.find_users_for_tracking(dt=now)
        print(users)
        for user in users:
            await self.start_track_dialog(
                user_id=user.id,
                period=user.period,
                timestamp=now.timestamp(),
            )

    async def start_track_dialog(
        self,
        user_id: int,
        period: int,
        timestamp: float,
    ) -> None:
        dm = self.manage_factory.bg(
            bot=self.bot,
            user_id=user_id,
            chat_id=user_id,
            load=False,
        )
        await dm.start(
            state=self.track_state,
            mode=StartMode.RESET_STACK,
            data={
                "period": period,
                "target_timestamp": timestamp,
            },
        )


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    settings = Settings()

    engine = create_engine(connection_uri=settings.build_db_connection_uri())
    session_factory = create_session_factory(engine=engine)

    bot = create_bot(settings=settings)

    storage = create_storage(settings=settings)
    dp = Dispatcher(storage=storage)
    dp.update.outer_middleware(SettingsMiddleware(settings=settings))
    dp.update.outer_middleware(DatabaseMiddleware(session_factory=session_factory))

    register_dialogs(dp)
    manager_factory = setup_dialogs(dp)
    async with session_factory() as session:
        notificator = ControllerNotificator(
            bot=bot,
            track_state=TrackSG.input_track_message,
            manager_factory=manager_factory,
            provider=DatabaseProvider(session=session),
        )
        await notificator.send_notifications()

    await asyncio.sleep(SLEEP_TIME)
    await bot.session.close()


if __name__ == "__main__":
    """Running in cron"""
    asyncio.run(main())
