from datetime import datetime, time
from typing import Any, NoReturn

from sqlalchemy import ScalarResult, and_, func, insert, or_, select
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.sql.functions import concat
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User
from src.db.repositories.base import Repository
from src.exceptions import TrackerBotError


class UserRepository(Repository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=User, session=session)

    async def get_by_id_or_none(
        self,
        user_id: int,
    ) -> User | None:
        return await self._get_by_id_or_none(obj_id=user_id)

    async def get_by_id(self, user_id: int) -> User:
        return await self._get_by_id(obj_id=user_id)

    async def create(
        self,
        *,
        user_id: int,
        period: int,
        time_zone: int,
        start_time: time,
        end_time: time,
        is_working: bool,
    ) -> User:
        query = (
            insert(User)
            .values(
                id=user_id,
                period=period,
                time_zone=time_zone,
                start_time=start_time,
                end_time=end_time,
                is_working=is_working,
            )
            .returning(User)
        )
        try:
            result: ScalarResult[User] = await self._session.scalars(
                select(User).from_statement(query),
            )
        except IntegrityError as e:
            await self._session.rollback()
            self._raise_error(e)
        else:
            await self._session.commit()
            return result.one()

    async def update(self, user_id: int, **kwargs: Any) -> User:
        try:
            return await self._update(User.id == user_id, **kwargs)
        except IntegrityError as e:
            await self._session.rollback()
            self._raise_error(e)

    def _raise_error(self, err: DBAPIError) -> NoReturn:
        raise TrackerBotError from err
