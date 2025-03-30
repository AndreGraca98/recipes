import datetime
import uuid

from sqlmodel import Field

__all__ = ("_CommonBase", "utc_now")


def utc_now():
    return datetime.datetime.now(tz=datetime.UTC)


class _CommonBase:
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
    )
    created_at: datetime.datetime = Field(default_factory=utc_now, nullable=False)
    updated_at: datetime.datetime | None = Field(
        default_factory=utc_now, sa_column_kwargs={"onupdate": utc_now}
    )
