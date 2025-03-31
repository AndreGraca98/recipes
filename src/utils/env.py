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

        # Filestore
        self.FILESTORE_ADDRESS: str = self._env.str("FILESTORE_ADDRESS")
        self.FILESTORE_ACCESS_KEY: str = self._env.str("FILESTORE_ACCESS_KEY")
        self.FILESTORE_SECRET_KEY: str = self._env.str("FILESTORE_SECRET_KEY")
        self.FILESTORE_BUCKET: str = self._env.str(
            "FILESTORE_BUCKET", default="recipes"
        ).lower()
        self.FILESTORE_REGION: str = self._env.str(
            "FILESTORE_REGION", default="us-east-1"
        ).lower()
        self.FILESTORE_USE_HTTPS: bool = self._env.bool(
            "FILESTORE_USE_HTTPS", default=False
        )
        self.FILESTORE_SHOULD_CREATE_BUCKET: bool = self._env.bool(
            "FILESTORE_SHOULD_CREATE_BUCKET", default=False
        )
