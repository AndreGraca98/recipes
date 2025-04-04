from fastapi import APIRouter

from ._tags import TAGS_METADATA  # noqa: F401
from .ingredient import router_v1 as ingredient_router_v1

# from .recipe import crud_router_v1 as recipe_crud_router_v1
# from .recipe import router_v1 as recipe_router_v1
# from .recipe_ingredient import crud_router_v1 as recipe_ingredient_crud_router_v1
# from .recipe_ingredient import router_v1 as recipe_ingredient_router_v1

__all__ = ["TAGS_METADATA", "ROUTERS"]

ROUTERS: list[APIRouter] = [
    ingredient_router_v1,
    # recipe_crud_router_v1,
    # recipe_router_v1,
    # recipe_ingredient_crud_router_v1,
    # recipe_ingredient_router_v1,
]
"""A list of all the routers for the service"""
