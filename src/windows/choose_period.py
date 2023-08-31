import csv
import io

from aiogram.types import BufferedInputFile, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const

from src.states import MainMenuSG, ReportGenerateSG


class ChoosePeriodWindow(Window):
    def __init__(self) -> None:
        super().__init__(
            Const("За какой период сгенерировать отчет?"),
            Row(
                Button(
                    text=Const("День"),
                    id="day_1",
                    on_click=generate_report,
                ),
                Button(text=Const("7 дней"), id="day_7", on_click=generate_report),
            ),
            state=ReportGenerateSG.choose_period,
        )


async def generate_report(
    c: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    days = int(button.widget_id.split("_")[1])
    prefix = "day" if days == 1 else "week"
    d = [
        ["Number", "Title", "Day"],
        [1, "asdfasdfadsf", 3],
        [2, "asdfas sadfhasdfkjasd kfajsdlfj asdf", 2],
        [3, "SErgey asdfasldkfja fljasdlfj asdf ", 3],
    ]
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerows(d)

    file = output.getvalue().encode()
    if c.bot is None:
        return
    await c.bot.send_message(chat_id=c.from_user.id, text="Отчет сформирован")
    await c.bot.send_document(
        document=BufferedInputFile(file=file, filename=f"last_{prefix}_report.csv"),
        chat_id=c.from_user.id,
    )
    await manager.start(
        MainMenuSG.main_menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )
