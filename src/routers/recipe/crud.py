import uuid
from typing import Annotated

from fastapi import APIRouter, Query
from sqlmodel import select

from src.models import Recipe
from src.models.recipe import RecipeCreate, RecipePublic, RecipeUpdate
from src.routers import _tags
from src.utils import SessionDependency, getLogger
from src.utils.responses import NotFoundResponse

_log = getLogger(__name__)

router_v1 = APIRouter(prefix="/v1/crud/recipes", tags=[_tags.V1, _tags.Recipe])


RecipeNotFoundResponse = NotFoundResponse("recipe not found")


@router_v1.get("", response_model=list[RecipePublic])
async def get_all_recipes(
    session: SessionDependency,
    _page: Annotated[int, Query(ge=0)] = 0,
    _per_page: Annotated[int, Query(ge=1)] = 25,
):
    _log.debug(f"Getting {_per_page} recipes from page {_page}")
    q = select(Recipe).offset(_page * _per_page).limit(_per_page)
    recipe = session.scalars(q).all()
    return recipe


@router_v1.post("", response_model=RecipePublic)
async def create_an_recipe(recipe: RecipeCreate, session: SessionDependency):
    _log.debug("Creating a recipe...")
    db_recipe = Recipe.model_validate(recipe)
    session.add(db_recipe)
    session.commit()
    session.refresh(db_recipe)
    return db_recipe


@router_v1.get("/{recipe_id}", response_model=RecipePublic)
async def get_an_recipe(recipe_id: uuid.UUID, session: SessionDependency):
    _log.debug("Getting a recipe...")
    if not (recipe := session.get(Recipe, recipe_id)):
        return RecipeNotFoundResponse
    return recipe


@router_v1.patch("/{recipe_id}", response_model=RecipePublic)
async def update_an_recipe(
    recipe_id: uuid.UUID, recipe: RecipeUpdate, session: SessionDependency
):
    if not (recipe_db := session.get(Recipe, recipe_id)):
        return RecipeNotFoundResponse
    recipe_data = recipe.model_dump(exclude_unset=True)
    recipe_db.sqlmodel_update(recipe_data)
    session.add(recipe_db)
    session.commit()
    session.refresh(recipe_db)
    return recipe_db


@router_v1.delete("/{recipe_id}")
async def delete_an_recipe(recipe_id: uuid.UUID, session: SessionDependency):
    if not (recipe_db := session.get(Recipe, recipe_id)):
        return RecipeNotFoundResponse
    session.delete(recipe_db)
    session.commit()
    return {"ok": True}
