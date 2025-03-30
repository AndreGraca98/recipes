from typing import Annotated, Any, Generator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import Session

from .env import Environment

__all__ = ["get_session", "SessionDependency"]

engine = create_engine(Environment().DATABASE_URL)
"""The SQLAlchemy engine to use for database operations"""


def get_session() -> Generator[Session, Any, None]:
    """Get a database session"""
    with Session(engine) as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_session)]
