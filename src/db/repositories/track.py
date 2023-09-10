from datetime import datetime
from typing import Any, NoReturn
from datetime import datetime, time
from typing import Any, NoReturn

from sqlalchemy import ScalarResult, and_, func, insert, or_, select
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.sql.functions import concat

from sqlalchemy import Date, ScalarResult, cast, insert, select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Track, User
from src.db.repositories.base import Repository
from src.dto import TrackDTO
from src.exceptions import TrackerBotError


class TrackRepository(Repository[Track]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Track, session=session)

    async def get_track_by_id(self, track_id: int) -> Track:
        return await self._get_by_id(obj_id=track_id)

    async def create_track(
        self,
        *,
        user_id: int,
        start_worked_at: datetime,
        end_worked_at: datetime,
        message: str | None = None,
    ) -> Track:
        query = (
            insert(Track)
            .values(
                user_id=user_id,
                start_worked_at=start_worked_at,
                end_worked_at=end_worked_at,
                message=message,
            )
            .returning(Track)
        )
        try:
            result: ScalarResult[Track] = await self._session.scalars(
                select(Track).from_statement(query),
            )
        except IntegrityError as e:
            await self._session.rollback()
            self._raise_error(e)
        else:
            await self._session.commit()
            return result.one()

    async def update_track_by_id(self, track_id: int, **kwargs: Any) -> Track:
        return await self._update(Track.id == track_id, **kwargs)

    async def export_track_by_last_days(
        self,
        user_id: int,
        days: int = 1,
    ) -> list[TrackDTO]:
        query = (
            select(Track)
            .where(Track.user_id == user_id, cast(Track.worked_at, Date))
            .order_by(Track.worked_at)
        )
        return [
            TrackDTO.model_validate(track)
            for track in (await self._session.scalars(query)).all()
        ]

    async def find_users_for_tracking(self, dt: datetime) -> list[Track]:
        offset = func.cast(concat(User.time_zone, " HOURS"), INTERVAL) - func.cast(
            concat(User.period, " MINUTES"), INTERVAL
        )

        query = select(Track).where(Track.ended_work_at < dt.time() + offset)
        return (await self._session.scalars(query)).all()

    def _raise_error(self, err: DBAPIError) -> NoReturn:
        raise TrackerBotError from err
