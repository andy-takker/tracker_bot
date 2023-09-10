from typing import TYPE_CHECKING

from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Format

from src.states import SettingsSG, TrackSG

if TYPE_CHECKING:
    from src.db.provider import DatabaseProvider


class TrackTimeWindow(Window):
    def __init__(self) -> None:
        super().__init__(
            Format("Напишите, чем вы занимались последние {period} минут?"),
            state=TrackSG.input_track_message,
        )


async def input_track_message_handler(
    m: Message,
    widget: MessageInput,
    manager: DialogManager,
) -> None:
    track_id = manager.dialog_data["track_id"]
    provider: DatabaseProvider = manager.middleware_data["provider"]
    await provider.track.update_track_by_id(track_id=track_id, message=str(m.text))
    await m.answer("Ответ записал.")
    await manager.done()
    await manager.start(state=SettingsSG.menu, mode=StartMode.RESET_STACK)
