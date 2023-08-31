from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from src.db.provider import DatabaseProvider
from src.states import MainMenuSG, RegistrationSG


async def start_command(
    message: Message,
    dialog_manager: DialogManager,
    provider: DatabaseProvider,
) -> None:
    if message.from_user is None:
        return
    user = await provider.user.read_by_id(message.from_user.id)
    if user is not None:
        await dialog_manager.start(MainMenuSG.main_menu, mode=StartMode.RESET_STACK)
    else:
        await message.answer(
            "Добро пожаловать!"
            " Чтобы начать трекинг времени нужно указать дополнительную информацию",
        )
        await dialog_manager.start(
            RegistrationSG.set_frequency,
            mode=StartMode.RESET_STACK,
        )
