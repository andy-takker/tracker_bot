from typing import TYPE_CHECKING, Any

from aiogram_dialog import Dialog, DialogManager

from src.db.schemas import StartTrackSchema
from src.windows.track_time import TrackTimeWindow

if TYPE_CHECKING:
    from src.db.provider import DatabaseProvider


def get_dialog() -> Dialog:
    return Dialog(
        TrackTimeWindow(),
        getter=dialog_getter,
        on_start=create_track_on_start,
    )


async def create_track_on_start(start_data: Any, manager: DialogManager) -> None:
    track_data = StartTrackSchema(**start_data)
    provider: DatabaseProvider = manager.middleware_data["provider"]
    track = await provider.track.create_track(
        user_id=track_data.user_id,
        start_worked_at=track_data.start_worked_at,
        end_worked_at=track_data.end_worked_at,
        message=None,
    )
    manager.dialog_data["track_id"] = track.id


async def dialog_getter(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, str | int | float]:
    return {"period": 30}
