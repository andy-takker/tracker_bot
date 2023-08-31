from aiogram_dialog import Dialog

from src.windows.choose_period import ChoosePeriodWindow


def get_dialog() -> Dialog:
    return Dialog(ChoosePeriodWindow())
