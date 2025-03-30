from typing import Any

from fastapi.responses import JSONResponse

__all__ = [
    "SuccessJSONResponse",
]


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
