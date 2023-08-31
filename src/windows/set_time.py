from collections.abc import Callable
from typing import Literal

from aiogram.fsm.state import State
from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const

from src.utils import check_time_str

TimeType = Literal["start_time", "end_time"]


FORMAT_MESSAGE = "Укaжитe ввиде - ЧЧ:MM"

MESSAGES = {
    "start_time": f"Bo сколько начать Bac спрашивать?\n{FORMAT_MESSAGE}",
    "end_time": f"Bo сколько закончить Bac спрашивать?{FORMAT_MESSAGE}",
}


class SetTimeWindow(Window):
    def __init__(
        self,
        state: State,
        key: TimeType,
        back_state: State | None = None,
    ) -> None:
        handler = time_handler(time_key=key)
        widgets = [
            Const(
                f"{MESSAGES[key]}\n",
            ),
            MessageInput(func=handler),
        ]
        if back_state is not None:
            widgets.append(
                SwitchTo(
                    text=Const(
                        "Назад",
                    ),
                    state=back_state,
                    id="back_to_menu",
                ),
            )
        super().__init__(
            *widgets,
            state=state,
        )


def time_handler(time_key: TimeType) -> Callable:
    async def input_time_handler(
        m: Message,
        widget: MessageInput,
        manager: DialogManager,
    ) -> None:
        if not check_time_str(m.text):
            await m.answer("Формат данных неверный")
            return
        if manager.start_data and manager.start_data.get("from") == "main_menu":
            await manager.done(result={time_key: m.text})
        else:
            manager.dialog_data[time_key] = m.text
            await manager.next()

    return input_time_handler
