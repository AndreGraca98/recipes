from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .env import Environment

__all__ = ["getSession"]

engine = create_engine(Environment().DATABASE_URL)
"""The SQLAlchemy engine to use for database operations"""

SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def getSession() -> Generator[Session, Any, None]:
    """Get a database session"""
    session = SessionMaker()
    try:
        yield session
    finally:
        session.close()
