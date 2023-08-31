from typing import TYPE_CHECKING, Any

from aiogram.types import CallbackQuery, User
from aiogram_dialog import DialogManager, ShowMode, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Row, Start
from aiogram_dialog.widgets.text import Const, Format

from src.states import MainMenuSG, WeekendSG

if TYPE_CHECKING:
    from src.db.provider import DatabaseProvider

STATUS = {
    True: "Работаю",
    False: "Выходной",
}


class WeekendWindow(Window):
    def __init__(self) -> None:
        super().__init__(
            Format(text="{question}"),
            Row(
                Start(
                    text=Const("Нет"),
                    id="settings_back",
                    state=MainMenuSG.main_menu,
                    mode=StartMode.RESET_STACK,
                ),
                Button(text=Const("Да"), id="approved", on_click=on_click_approved),
            ),
            state=WeekendSG.change_status,
            getter=get_weekend_data,
        )


async def on_click_approved(
    c: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    provider: DatabaseProvider = manager.middleware_data["provider"]
    old_user = await provider.user.get_by_id(user_id=c.from_user.id)
    user = await provider.user.update(
        user_id=c.from_user.id,
        is_working=not old_user.is_working,
    )

    status = STATUS[user.is_working]
    manager.show_mode = ShowMode.SEND
    await c.message.answer(text=f"Статус был изменен на `{status}`")
    await manager.done()
    manager.show_mode = ShowMode.EDIT


async def get_weekend_data(
    dialog_manager: DialogManager,
    event_from_user: User,
    **kwargs: dict[str, Any],
) -> dict[str, str | int | float]:
    provider: DatabaseProvider = dialog_manager.middleware_data["provider"]
    user = await provider.user.get_by_id(user_id=event_from_user.id)
    return {
        "question": "Ваш текущий статус `{}`. Поменять ero на `{}`?".format(
            STATUS[user.is_working],
            STATUS[not user.is_working],
        ),
    }
