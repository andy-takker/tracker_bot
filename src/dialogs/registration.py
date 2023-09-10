from aiogram_dialog import Dialog

from src.states import RegistrationSG
from src.windows.confirm import ConfirmRegistrationWindow
from src.windows.set_period import SetFrequencyWindow
from src.windows.set_time import SetTimeWindow
from src.windows.set_time_zone import SetTimeZoneWindow


def get_dialog() -> Dialog:
    return Dialog(
        SetFrequencyWindow(
            state=RegistrationSG.set_period,
        ),
        SetTimeZoneWindow(state=RegistrationSG.set_time_zone),
        SetTimeWindow(state=RegistrationSG.set_start_time, key="start_time"),
        SetTimeWindow(state=RegistrationSG.set_end_time, key="end_time"),
        ConfirmRegistrationWindow(state=RegistrationSG.confirm),
    )
