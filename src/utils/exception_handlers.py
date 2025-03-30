import re

import sqlalchemy

from .logger import getLogger
from .responses.error import DuplicatedEntry, ServerExceptionResponse

_log = getLogger(__name__)

INTEGRITY_ERROR_PATTERN_RESPONSE_MAPPING = {
    re.compile(
        r"\d+, \"Duplicate entry '(?P<value>.*)' for key '(?P<column>.*)'"
    ): DuplicatedEntry
}
"""Mapping from integrity error regex to a response class."""


def handle_integrity_error(exc: sqlalchemy.exc.IntegrityError, ctx: dict):
    for pattern, response in INTEGRITY_ERROR_PATTERN_RESPONSE_MAPPING.items():
        if extracted_error := pattern.search(str(exc)):
            return response(**extracted_error.groupdict(), ctx=ctx)  # type: ignore
    # pattern for this particular exception was not found. using normal server exception
    exc_str = str(exc)
    _log.warning(
        f'No handler found for pattern "{exc_str[:15]}..." . Defaulting to server exception response'
    )
    return ServerExceptionResponse(error=exc, error_details=ctx)
