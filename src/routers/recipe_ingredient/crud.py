import uuid
from typing import Annotated

from fastapi import APIRouter, Query
from sqlmodel import select

from src.models import RecipeIngredient
from src.models.recipe_ingredient import (
    RecipeIngredientCreate,
    RecipeIngredientPublic,
    RecipeIngredientUpdate,
)
from src.routers import _tags
from src.utils import SessionDependency, getLogger
from src.utils.responses import NotFoundResponse

_log = getLogger(__name__)

router_v1 = APIRouter(
    prefix="/v1/crud/recipe-ingredients", tags=[_tags.V1, _tags.RecipeIngredient]
)


RecipeIngredientNotFoundResponse = NotFoundResponse("recipe ingredient not found")


@router_v1.get("", response_model=list[RecipeIngredientPublic])
async def get_all_recipe_ingredients(
    session: SessionDependency,
    _page: Annotated[int, Query(ge=0)] = 0,
    _per_page: Annotated[int, Query(ge=1)] = 25,
):
    _log.debug(f"Getting {_per_page} recipe ingredients from page {_page}")
    q = select(RecipeIngredient).offset(_page * _per_page).limit(_per_page)
    ingredient = session.scalars(q).all()
    return ingredient


@router_v1.post("", response_model=RecipeIngredientPublic)
async def create_an_recipe_ingredient(
    ingredient: RecipeIngredientCreate, session: SessionDependency
):
    _log.debug("Creating a recipe ingredient...")
    db_recipe_ingredient = RecipeIngredient.model_validate(ingredient)
    session.add(db_recipe_ingredient)
    session.commit()
    session.refresh(db_recipe_ingredient)
    return db_recipe_ingredient


@router_v1.get("/{recipe_ingredient_id}", response_model=RecipeIngredientPublic)
async def get_an_recipe_ingredient(
    recipe_ingredient_id: uuid.UUID, session: SessionDependency
):
    _log.debug("Getting a recipe ingredient...")
    if not (ingredient := session.get(RecipeIngredient, recipe_ingredient_id)):
        return RecipeIngredientNotFoundResponse
    return ingredient


@router_v1.patch("/{recipe_ingredient_id}", response_model=RecipeIngredientPublic)
async def update_an_recipe_ingredient(
    recipe_ingredient_id: uuid.UUID,
    ingredient: RecipeIngredientUpdate,
    session: SessionDependency,
):
    if not (ingredient_db := session.get(RecipeIngredient, recipe_ingredient_id)):
        return RecipeIngredientNotFoundResponse
    ingredient_data = ingredient.model_dump(exclude_unset=True)
    ingredient_db.sqlmodel_update(ingredient_data)
    session.add(ingredient_db)
    session.commit()
    session.refresh(ingredient_db)
    return ingredient_db


@router_v1.delete("/{recipe_ingredient_id}")
async def delete_an_recipe_ingredient(
    recipe_ingredient_id: uuid.UUID, session: SessionDependency
):
    if not (ingredient_db := session.get(RecipeIngredient, recipe_ingredient_id)):
        return RecipeIngredientNotFoundResponse
    session.delete(ingredient_db)
    session.commit()
    return {"ok": True}
