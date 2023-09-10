from typing import Any
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo
from aiogram_dialog.widgets.text import Const

from src.db.models import Frequency


class SetFrequencyWindow(Window):
    def __init__(self, state: State, back_state: State | None = None) -> None:
        self.back_state = back_state
        row = Row(
            *[
                Button(
                    text=Const(f"{f.value}"),
                    id=f"period_{f}",
                    on_click=save_period,
                )
                for f in Frequency
            ],
        )
        super().__init__(
            Const("Как часто y Bac спрашивать статус?"),
            row,
            SwitchTo(
                id="back_to_menu",
                text=Const("Назад"),
                state=back_state,  # type: ignore[arg-type]
                when=self.has_back_state,  # type: ignore[arg-type]
            ),
            state=state,
        )

    def has_back_state(self, *args: Any, **kwargs: Any) -> bool:
        return self.back_state is not None


async def save_period(
    c: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    if button.widget_id is None:
        return
    period = int(button.widget_id.split("_")[1])
    if manager.start_data and manager.start_data.get("from") == "main_menu":
        await manager.done(result={"period": period})
    else:
        manager.dialog_data["period"] = period
        await manager.next()
