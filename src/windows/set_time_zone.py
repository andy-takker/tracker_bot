from typing import Any

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Group, SwitchTo
from aiogram_dialog.widgets.text import Const

from src.db.models import UTC_END, UTC_START
from src.utils import format_tz

SPEC_CONST = 100


class SetTimeZoneWindow(Window):
    def __init__(self, state: State, back_state: State | None = None) -> None:
        self.back_state = back_state
        keyboard = self.get_utc_keyboard()
        super().__init__(
            Const("В каком Вы часовом поясе по UTC?"),
            keyboard,
            SwitchTo(
                text=Const("Назад"),
                state=back_state,  # type: ignore[arg-type]
                when=self.has_back_state,  # type: ignore[arg-type]
                id="back_to_menu",
            ),
            state=state,
        )

    @staticmethod
    def get_utc_keyboard() -> Group:
        buttons = [
            Button(
                text=Const(format_tz(utc)),
                id=f"utc_{utc+SPEC_CONST}",
                on_click=on_utc_click,
            )
            for utc in range(UTC_START, UTC_END + 1)
        ]
        return Group(*buttons, width=6)

    def has_back_state(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        return self.back_state is not None


async def on_utc_click(
    c: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    if button.widget_id is None:
        return
    time_zone = int(button.widget_id.split("_")[1]) - SPEC_CONST
    if manager.start_data and manager.start_data.get("from") == "main_menu":
        await manager.done(result={"time_zone": time_zone})
    else:
        manager.dialog_data["time_zone"] = time_zone
        await manager.next()
