from typing import Literal

from environs import Env
from marshmallow.validate import OneOf

__all__ = ["Environment"]


class Environment:
    def __init__(self) -> None:
        self._env = Env()
        self._env.read_env()

        self.LOG_LEVEL: Literal["TRACE", "DEBUG", "INFO", "WARNING", "ERROR"] = (
            self._env.str(
                "LOG_LEVEL",
                "INFO",
                validate=OneOf(["TRACE", "DEBUG", "INFO", "WARNING", "ERROR"]),
            )
        )

        # Database
        self.DATABASE_URL: str = self._env.str("DATABASE_URL")
