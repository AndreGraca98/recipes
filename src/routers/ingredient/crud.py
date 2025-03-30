import uuid
from typing import Annotated

from fastapi import APIRouter, Query
from sqlmodel import select

from src.models import Ingredient
from src.models.ingredient import IngredientCreate, IngredientPublic, IngredientUpdate
from src.routers import _tags
from src.utils import SessionDependency, getLogger
from src.utils.responses import NotFoundResponse

_log = getLogger(__name__)

router_v1 = APIRouter(prefix="/v1/crud/ingredients", tags=[_tags.V1, _tags.Ingredient])


IngredientNotFoundResponse = NotFoundResponse("ingredient not found")


@router_v1.get("", response_model=list[IngredientPublic])
async def get_all_ingredients(
    session: SessionDependency,
    _page: Annotated[int, Query(ge=0)] = 0,
    _per_page: Annotated[int, Query(ge=1)] = 25,
):
    _log.debug(f"Getting {_per_page} ingredients from page {_page}")
    q = select(Ingredient).offset(_page).limit(_per_page)
    ingredient = session.scalars(q).all()
    return ingredient


@router_v1.post("", response_model=IngredientPublic)
async def create_an_ingredient(
    ingredient: IngredientCreate, session: SessionDependency
):
    _log.debug("Creating a ingredient...")
    db_ingredient = Ingredient.model_validate(ingredient)
    session.add(db_ingredient)
    session.commit()
    session.refresh(db_ingredient)
    return db_ingredient


@router_v1.get("/{ingredient_id}", response_model=IngredientPublic)
async def get_an_ingredient(ingredient_id: uuid.UUID, session: SessionDependency):
    _log.debug("Getting a ingredient...")
    if not (ingredient := session.get(Ingredient, ingredient_id)):
        return IngredientNotFoundResponse
    return ingredient


@router_v1.patch("/{ingredient_id}", response_model=IngredientPublic)
async def update_an_ingredient(
    ingredient_id: uuid.UUID, ingredient: IngredientUpdate, session: SessionDependency
):
    if not (ingredient_db := session.get(Ingredient, ingredient_id)):
        return IngredientNotFoundResponse
    ingredient_data = ingredient.model_dump(exclude_unset=True)
    ingredient_db.sqlmodel_update(ingredient_data)
    session.add(ingredient_db)
    session.commit()
    session.refresh(ingredient_db)
    return ingredient_db


@router_v1.delete("/{ingredient_id}")
async def delete_an_ingredient(ingredient_id: uuid.UUID, session: SessionDependency):
    if not (ingredient_db := session.get(Ingredient, ingredient_id)):
        return IngredientNotFoundResponse
    session.delete(ingredient_db)
    session.commit()
    return {"ok": True}
