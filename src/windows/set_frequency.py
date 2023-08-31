from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo
from aiogram_dialog.widgets.text import Const

from src.db.models import Frequency


class SetFrequencyWindow(Window):
    def __init__(self, state: State, back_state: State | None = None) -> None:
        row = Row(
            *[
                Button(
                    text=Const(f"{f.value}"),
                    id=f"frequency_{f}",
                    on_click=save_frequency,
                )
                for f in Frequency
            ],
        )
        self.widgets = [
            Const("Как часто y Bac спрашивать статус?"),
            row,
        ]
        if back_state is not None:
            self.add_back_button(back_state=back_state)
        super().__init__(
            *self.widgets,
            state=state,
        )

    def add_back_button(self, back_state: State) -> None:
        self.widgets.append(
            SwitchTo(
                text=Const(
                    "Назад",
                ),
                state=back_state,
                id="back_to_menu",
            ),
        )


async def save_frequency(
    c: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    if button.widget_id is None:
        return
    frequency = int(button.widget_id.split("_")[1])
    if manager.start_data and manager.start_data.get("from") == "main_menu":
        await manager.done(result={"frequency": frequency})
    else:
        manager.dialog_data["frequency"] = frequency
        await manager.next()
