from typing import Any

from fastapi.responses import JSONResponse
from fastapi import status

__all__ = [
    "BadRequestJSONResponse",
    "NotFoundJSONResponse",
    "ExceptionJSONResponse",
]


class BadRequestJSONResponse(JSONResponse):
    def __init__(self, message: str, ctx: dict[str, Any] | None = None, **kwargs):
        content = dict(message=message, ctx=ctx if ctx is not None else {})
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, content=content, **kwargs
        )


class NotFoundJSONResponse(JSONResponse):
    def __init__(self, message: str, ctx: dict[str, Any] | None = None, **kwargs):
        content = dict(message=message, ctx=ctx if ctx is not None else {})
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, content=content, **kwargs
        )


class ExceptionJSONResponse(JSONResponse):
    def __init__(
        self,
        status_code: int,
        error: BaseException,
        error_details: dict[str, Any] | None = None,
        **kwargs,
    ):
        content = dict(
            error=str(error),
            error_type=type(error).__name__,
            error_details=error_details if error_details is not None else {},
        )
        super().__init__(status_code=status_code, content=content, **kwargs)
