from datetime import time

from pydantic import BaseModel, conint

from src.db.models import UTC_END, UTC_START, Frequency


class UpdateUser(BaseModel):
    frequency: Frequency | None = None
    time_zone: conint(strict=True, ge=UTC_START, le=UTC_END) | None = None  # type: ignore[valid-type]
    start_time: time | None = None
    end_time: time | None = None
