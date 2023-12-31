from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.track import TrackRepository
from src.db.repositories.user import UserRepository


class DatabaseProvider:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user = UserRepository(session=session)
        self.track = TrackRepository(session=session)
