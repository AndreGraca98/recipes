from functools import partial
from pathlib import Path
from typing import Any

from fastapi import BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse

from ..logger import getLogger

__all__ = ["SuccessJSONResponse", "SelfDestructFileResponse"]

_log = getLogger(__name__)


class SuccessJSONResponse(JSONResponse):
    def __init__(
        self,
        status_code: int,
        message: str,
        ctx: dict[str, Any] | None = None,
        **kwargs,
    ):
        content = dict(message=message, ctx=ctx if ctx is not None else {})
        super().__init__(status_code=status_code, content=content, **kwargs)


class SelfDestructFileResponse(FileResponse):
    """FileResponse that deletes the file after it has been sent."""

    def __init__(
        self, path: Path, media_type: str, background_tasks: BackgroundTasks
    ) -> None:
        background_tasks.add_task(partial(path.unlink, missing_ok=True))
        self.path = path
        super().__init__(path, media_type=media_type)
