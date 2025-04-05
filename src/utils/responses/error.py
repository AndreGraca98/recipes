from typing import Any, Mapping, NotRequired, TypedDict, Unpack

from fastapi import status
from fastapi.responses import JSONResponse
from starlette.background import BackgroundTask

__all__ = [
    "BadRequestResponse",
    "NotFoundResponse",
    "ServerExceptionResponse",
]


class _ResponseKwargs(TypedDict):
    headers: NotRequired[Mapping[str, str] | None]
    media_type: NotRequired[str | None]
    background: NotRequired[BackgroundTask | None]


class BadRequestResponse(JSONResponse):
    """HTTP_400_BAD_REQUEST"""

    def __init__(
        self,
        message: str,
        ctx: dict[str, Any] | None = None,
        **kwargs: Unpack[_ResponseKwargs],
    ):
        content = dict(message=message, ctx=_null_to_dict(ctx))
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, content=content, **kwargs
        )


class NotFoundResponse(JSONResponse):
    """HTTP_404_NOT_FOUND"""

    def __init__(
        self,
        message: str,
        ctx: dict[str, Any] | None = None,
        **kwargs: Unpack[_ResponseKwargs],
    ):
        content = dict(message=message, ctx=_null_to_dict(ctx))
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, content=content, **kwargs
        )


class ServerExceptionResponse(JSONResponse):
    """HTTP_500_INTERNAL_SERVER_ERROR"""

    def __init__(
        self,
        error: BaseException,
        error_details: dict[str, Any] | None = None,
        **kwargs: Unpack[_ResponseKwargs],
    ):
        content = dict(
            error=str(error),
            error_type=type(error).__name__,
            error_details=_null_to_dict(error_details),
        )
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=content, **kwargs
        )


def _null_to_dict(value: None | dict) -> dict:
    if value is None:
        return {}
    assert isinstance(value, dict)
    return value


# Specialized responses
class DuplicatedEntryResponse(BadRequestResponse):
    def __init__(
        self,
        value: str,
        column: str,
        ctx: dict[str, Any] | None = None,
        **kwargs: Unpack[_ResponseKwargs],
    ):
        message = f"{value!r} already exists in {column!r}"
        super().__init__(message=message, ctx=ctx, **kwargs)
