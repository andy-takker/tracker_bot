from datetime import time
from typing import Any, NoReturn

from sqlalchemy import ScalarResult, insert, select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User
from src.db.repositories.base import Repository
from src.exceptions import TrackerBotError


class UserRepository(Repository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=User, session=session)

    async def read_by_id(self, user_id: int, strict: bool = False) -> User | None:
        user = await self._read_by_id(obj_id=user_id)
        if strict and user is None:
            raise TrackerBotError
        return user

    async def get_by_id(self, user_id: int) -> User:
        return await self.read_by_id(user_id=user_id, strict=True)  # type: ignore[return-value]

    async def create(
        self,
        user_id: int,
        frequency: int,
        time_zone: int,
        start_time: time,
        end_time: time,
        is_working: bool,
    ) -> User:
        query = (
            insert(User)
            .values(
                id=user_id,
                frequency=frequency,
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

    async def update(self, user_id: int, **kwargs: dict[str, Any]) -> User:
        try:
            return await self._update(User.id == user_id, **kwargs)
        except IntegrityError as e:
            await self._session.rollback()
            self._raise_error(e)

    def _raise_error(self, err: DBAPIError) -> NoReturn:
        raise TrackerBotError from err
