import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, File, Query, UploadFile
from sqlmodel import Session, select

from src.models import Ingredient
from src.models.ingredient import (
    IngredientCreate,
    IngredientPublic,
    IngredientUpdate,
)
from src.routers import _tags
from src.utils import SessionDependency, get_session, getLogger
from src.utils.filestore import FileType, download_object, upload_to_filestore
from src.utils.responses import (
    BadRequestResponse,
    NotFoundResponse,
)

from ...utils.responses.success import SelfDestructFileResponse
from .helpers import normalize_str

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
    q = select(Ingredient).offset(_page * _per_page).limit(_per_page)
    ingredient = session.scalars(q).all()
    return ingredient


@router_v1.post("", response_model=IngredientPublic)
async def create_an_ingredient(
    ingredient: IngredientCreate = Depends(),
    file: UploadFile = File(None),
    session: Session = Depends(get_session),
):
    _log.debug("Creating a ingredient...")

    db_ingredient = Ingredient.model_validate(ingredient)
    if f := file.file:
        assert (filename := file.filename)
        upload_to_filestore(f, filename, FileType.JPEG)
        db_ingredient.object_name = filename
    db_ingredient.normalized_name = normalize_str(db_ingredient.name)
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


@router_v1.get("/{ingredient_id}/image")
async def get_an_ingredient_image(
    ingredient_id: uuid.UUID,
    session: SessionDependency,
    background_tasks: BackgroundTasks,
):
    _log.debug("Getting a ingredient image")
    if not (ingredient := session.get(Ingredient, ingredient_id)):
        return IngredientNotFoundResponse
    if (object_name := ingredient.object_name) is None:
        return BadRequestResponse(f"ingredient={ingredient_id} does not have an image")
    with download_object(object_name, with_cleanup=False) as f:
        return SelfDestructFileResponse(
            f,
            # media_type=FileType.JPEG,
            media_type="image/png",
            background_tasks=background_tasks,
        )


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
