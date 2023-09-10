from aiogram_dialog import Dialog

from src.states import SettingsSG
from src.windows.set_period import SetFrequencyWindow
from src.windows.set_time import SetTimeWindow
from src.windows.set_time_zone import SetTimeZoneWindow
from src.windows.settings import SettingsWindow


def get_dialog() -> Dialog:
    return Dialog(
        SettingsWindow(),
        SetFrequencyWindow(
            state=SettingsSG.change_period,
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
