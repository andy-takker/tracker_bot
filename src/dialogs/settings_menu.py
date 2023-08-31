from aiogram_dialog import Dialog, StartMode, Window, DialogManager
from aiogram_dialog.widgets.kbd import Start, SwitchTo
from aiogram_dialog.widgets.text import Const

from src.states import MainMenuSG, SettingsSG
from src.windows.set_frequency import SetFrequencyWindow
from src.windows.set_time import SetTimeWindow
from src.windows.set_time_zone import SetTimeZoneWindow
from src.windows.settings import SettingsWindow


def get_dialog() -> Dialog:
    return Dialog(
        SettingsWindow(),
        SetFrequencyWindow(
            state=SettingsSG.change_frequency,
            back_state=SettingsSG.menu,
        ),
        SetTimeZoneWindow(
            state=SettingsSG.change_time_zone,
            back_state=SettingsSG.menu,
        ),
        SetTimeWindow(
            state=SettingsSG.change_start_time,
            key="start_time",
            back_state=SettingsSG.menu,
        ),
        SetTimeWindow(
            state=SettingsSG.change_end_time,
            key="end_time",
            back_state=SettingsSG.menu,
        ),
    )


