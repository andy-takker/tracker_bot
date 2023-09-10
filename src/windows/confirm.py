from typing import TYPE_CHECKING, Any

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from src.states import MainMenuSG
from src.utils import format_tz, parse_time_str

if TYPE_CHECKING:
    from src.db.provider import DatabaseProvider

FORMAT_TEMPLATE = """Ваш профиль:
Как часто спрашивать? Каждые {period} мин
Часовой пояс: {time_zone}
Время начала рабочего дня: {start_time}
Время конца рабочего дня: {end_time}
"""


class ConfirmRegistrationWindow(Window):
    def __init__(
        self,
        state: State,
    ) -> None:
        super().__init__(
            Format(text=FORMAT_TEMPLATE),
            Button(Const("Продолжить"), id="confirm", on_click=confirm_registration),
            state=state,
            getter=get_confirm_data,
        )


async def confirm_registration(
    c: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    provider: DatabaseProvider = manager.middleware_data["provider"]

    await provider.user.create(
        user_id=c.from_user.id,
        period=manager.dialog_data["period"],
        start_time=parse_time_str(manager.dialog_data["start_time"]).time(),
        end_time=parse_time_str(manager.dialog_data["end_time"]).time(),
        time_zone=manager.dialog_data["time_zone"],
        is_working=True,
    )
    await manager.done()
    await manager.start(MainMenuSG.main_menu, mode=StartMode.RESET_STACK)


async def get_confirm_data(
    dialog_manager: DialogManager,
    **kwargs: dict[str, Any],
) -> dict[str, str | int | float]:
    tz = dialog_manager.dialog_data["time_zone"]
    start_time = parse_time_str(dialog_manager.dialog_data["start_time"]).strftime(
        "%H:%M",
    )
    end_time = parse_time_str(dialog_manager.dialog_data["end_time"]).strftime("%H:%M")

    return {
        "period": dialog_manager.dialog_data["period"],
        "time_zone": format_tz(tz),
        "start_time": start_time,
        "end_time": end_time,
    }
