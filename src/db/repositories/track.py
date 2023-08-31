from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Track
from src.db.repositories.base import Repository


class TrackRepository(Repository[Track]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Track, session=session)

    async def export_track_by_last_days(
        self,
        user_id: int,
        days: int = 1,
    ) -> Sequence[Track]:
        query = select(Track).where(Track.user_id == user_id).order_by(Track.worked_at)
        return (await self._session.scalars(query)).all()
