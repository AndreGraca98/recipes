import uuid

from fastapi import APIRouter

from src.models import RecipeIngredient
from src.utils import SessionDependency, getLogger

from .. import _tags
from .crud import RecipeIngredientNotFoundResponse

_log = getLogger(__name__)

router_v1 = APIRouter(
    prefix="/v1/recipe-ingredients", tags=[_tags.V1, _tags.RecipeIngredient]
)


@router_v1.post("/{recipe_ingredient_id}")
async def get_human_readable_recipe_ingredient(
    recipe_ingredient_id: uuid.UUID, session: SessionDependency
):
    _log.debug("Getting a recipe ingredient...")
    if not (recipe_ingredient := session.get(RecipeIngredient, recipe_ingredient_id)):
        return RecipeIngredientNotFoundResponse

    match recipe_ingredient.unit:
        case "g":
            ...
    return dict(
        name=recipe_ingredient.ingredient.name,
        # unit=unit,
        quantity=recipe_ingredient.quantity,
    )


def normalize_unit(unit: str) -> str:
    return unit.lower().strip()
