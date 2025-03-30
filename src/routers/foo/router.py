from fastapi import APIRouter

from src.utils import getLogger

from .helpers import BAR
from .._tags import FOO

_log = getLogger(__name__)

router_v1 = APIRouter(prefix="/v1/foo", tags=[FOO])


@router_v1.get("")
async def get_a_foo():
    _log.debug("Getting a foo")
    return dict(foo=BAR)
