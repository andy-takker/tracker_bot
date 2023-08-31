from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from src.states import MainMenuSG, ReportGenerateSG, SettingsSG, WeekendSG


class MainMenuWindow(Window):
    def __init__(self) -> None:
        super().__init__(
            Const("Главное меню"),
            Start(
                text=Const("Отчет"),
                id="report",
                state=ReportGenerateSG.choose_period,
            ),
            Start(
                text=Const("Выходной"),
                id="weekend",
                state=WeekendSG.change_status,
            ),
            Start(
                text=Const("Настройки"),
                id="settings",
                state=SettingsSG.menu,
                data={"from": "main_menu"},
            ),
            state=MainMenuSG.main_menu,
        )
