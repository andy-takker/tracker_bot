from aiogram_dialog import Dialog

from src.windows.weekend import WeekendWindow


def get_dialog() -> Dialog:
    return Dialog(WeekendWindow())
