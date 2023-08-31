from typing import TYPE_CHECKING

from aiogram_dialog import Data, Dialog, DialogManager, ShowMode, StartMode

from src.db.schemas import UpdateUser
from src.states import MainMenuSG
from src.windows.main_menu import MainMenuWindow

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.types import User

    from src.db.provider import DatabaseProvider


async def main_menu_process_result(
    start_data: Data,
    result: dict,
    manager: DialogManager,
) -> None:
    if not result:
        return
    update_user_data = UpdateUser(**result)
    provider: DatabaseProvider = manager.middleware_data["provider"]
    user: User = manager.middleware_data["event_from_user"]
    await provider.user.update(
        user_id=user.id,
        **update_user_data.model_dump(exclude_none=True),
    )
    bot: Bot = manager.middleware_data["bot"]
    await bot.send_message(chat_id=user.id, text="Данные обновлены")
    await manager.start(
        MainMenuSG.main_menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )


def get_dialog() -> Dialog:
    main_menu_window = MainMenuWindow()
    return Dialog(
        main_menu_window,
        on_process_result=main_menu_process_result,
    )
