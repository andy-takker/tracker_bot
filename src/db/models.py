import enum
from datetime import datetime, time

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Time,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import ChoiceType

from src.db.base import Base
from src.db.mixins import TimestampMixin


class Frequency(enum.IntEnum):
    QUARTER = 15
    THIRD = 20
    HALF = 30
    HOUR = 60


UTC_START, UTC_END = -11, 12


class User(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    frequency: Mapped[int] = mapped_column(
        ChoiceType(Frequency, impl=Integer()),
        nullable=False,
        index=True,
    )
    time_zone: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    is_working: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class Track(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("user.id"),
        nullable=False,
        index=True,
    )
    worked_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    message: Mapped[str] = mapped_column(String(300), nullable=True)


class MessageType(enum.StrEnum):
    PRAISE = "PRAISE"
    REGRET = "REGRET"


class SystemMessage(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[str] = mapped_column(String(1024), nullable=False)
    mtype: Mapped[str] = mapped_column(
        ChoiceType(MessageType, impl=String(16)),
        nullable=False,
        index=True,
    )
