from datetime import datetime

from pydantic import BaseModel, ConfigDict

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class TrackDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    started_work_at: datetime
    ended_work_at: datetime
    message: str | None

    def to_csv_row(self) -> list[str]:
        return [
            self.started_work_at.strftime(DATETIME_FORMAT),
            self.ended_work_at.strftime(DATETIME_FORMAT),
            self.message or "",
        ]

    @staticmethod
    def header() -> list[str]:
        return ["started_work_at", "ended_work_at", "message"]
