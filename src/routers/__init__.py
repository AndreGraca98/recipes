from fastapi import APIRouter

from ._tags import TAGS_METADATA  # noqa: F401
from .ingredient import crud_router_v1 as ingredient_crud_router_v1
from .ingredient import router_v1 as ingredient_router_v1

__all__ = ["TAGS_METADATA", "ROUTERS"]

ROUTERS: list[APIRouter] = [
    ingredient_router_v1,
    ingredient_crud_router_v1,
]
"""A list of all the routers for the service"""
