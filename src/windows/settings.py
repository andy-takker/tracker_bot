from typing import TYPE_CHECKING, Any
from aiogram_dialog import StartMode, Window, DialogManager
from aiogram_dialog.widgets.kbd import Start, SwitchTo
from aiogram_dialog.widgets.text import Const, Format
from src.db.provider import DatabaseProvider

from src.states import MainMenuSG, SettingsSG
from src.utils import format_tz
if TYPE_CHECKING:
    from src.db.provider import DatabaseProvider
FORMAT_TEMPLATE = """Настройки

Как часто спрашивать? Каждые {frequency} мин
Часовой пояс: {time_zone}
Время начала рабочего дня: {start_time}
Время конца рабочего дня: {end_time}
"""

class SettingsWindow(Window):
    def __init__(self) -> None:
        super().__init__(
            Format(FORMAT_TEMPLATE),
            SwitchTo(
                text=Const("Изменить период отправки сообщений"),
                id="settings_change_frequency",
                state=SettingsSG.change_frequency,
            ),
            SwitchTo(
                text=Const("Изменить часовой пояс"),
                id="settings_change_time_zone",
                state=SettingsSG.change_time_zone,
            ),
            SwitchTo(
                text=Const("Изменить время начала"),
                id="settings_change_start_time",
                state=SettingsSG.change_start_time,
            ),
            SwitchTo(
                text=Const("Изменить время окончания"),
                id="settings_change_end_time",
                state=SettingsSG.change_end_time,
            ),
            Start(
                text=Const("B главное меню"),
                id="settings_back",
                state=MainMenuSG.main_menu,
                mode=StartMode.RESET_STACK,
            ),
            state=SettingsSG.menu,
            getter=get_settings_data,
        )

async def get_settings_data(
    dialog_manager: DialogManager,
    **kwargs: dict[str, Any],
) -> dict[str, str | int | float]:
    provider: DatabaseProvider = dialog_manager.middleware_data['provider']
    from_user = dialog_manager.middleware_data['event_from_user']
    user = await provider.user.get_by_id(from_user.id)
    return {
        "frequency": user.frequency,
        "time_zone": format_tz(user.time_zone),
        "start_time": "{:02d}:{:02d}".format(user.start_time.hour, user.start_time.minute),
        "end_time": "{:02d}:{:02d}".format(user.end_time.hour, user.end_time.minute),
    }
