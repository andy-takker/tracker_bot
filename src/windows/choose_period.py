from typing import TYPE_CHECKING

from aiogram.types import BufferedInputFile, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Row, Group, Cancel
from aiogram_dialog.widgets.text import Const

from src.states import MainMenuSG, ReportGenerateSG
from src.utils import generate_report_file

if TYPE_CHECKING:
    from src.db.provider import DatabaseProvider


class ChoosePeriodWindow(Window):
    def __init__(self) -> None:
        super().__init__(
            Const("За какой период сгенерировать отчет?"),
            Group(
                Row(
                    Button(
                        text=Const("День"),
                        id="day_1",
                        on_click=generate_report,
                    ),
                    Button(text=Const("7 дней"), id="day_7", on_click=generate_report),
                ),
                Cancel(text=Const("Назад")),
            ),
            state=ReportGenerateSG.choose_period,
        )


async def generate_report(
    c: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    if c.bot is None:
        return
    if button.widget_id is None:
        return
    provider: DatabaseProvider = manager.middleware_data["provider"]

    days = int(button.widget_id.split("_")[1])
    tracks = await provider.track.export_track_by_last_days(
        user_id=manager.middleware_data["event_from_user"],
        days=days,
    )
    csv_file = generate_report_file(tracks=tracks)

    await c.bot.send_message(chat_id=c.from_user.id, text="Отчет сформирован")
    await c.bot.send_document(
        document=BufferedInputFile(file=csv_file, filename="report.csv"),
        chat_id=c.from_user.id,
    )
    await manager.start(
        MainMenuSG.main_menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )
