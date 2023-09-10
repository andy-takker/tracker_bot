from datetime import datetime, time

from pydantic import BaseModel, conint

from src.db.models import UTC_END, UTC_START, Frequency

TimeZoneType = conint(strict=True, ge=UTC_START, le=UTC_END)


class UpdateUser(BaseModel):
    period: Frequency | None = None
    time_zone: TimeZoneType | None = None  # type: ignore[valid-type]
    start_time: time | None = None
    end_time: time | None = None


class StartTrackSchema(BaseModel):
    start_worked_at: datetime
    end_worked_at: datetime
    period: int
    user_id: int
