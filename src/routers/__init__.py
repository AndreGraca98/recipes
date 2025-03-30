from fastapi import APIRouter

from ._tags import TAGS_METADATA  # noqa: F401
from .foo import router_v1 as foo_router_v1

__all__ = ["TAGS_METADATA", "ROUTERS"]

ROUTERS: list[APIRouter] = [foo_router_v1]
"""A list of all the routers for the service"""
