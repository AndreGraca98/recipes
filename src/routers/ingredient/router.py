import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, File, Query, UploadFile
from sqlalchemy import update
from sqlmodel import Session, select

from src.models import Ingredient
from src.models.ingredient import (
    IngredientCreate,
    IngredientPublic,
    IngredientUpdate,
)
from src.routers import _tags
from src.utils import SessionDependency, get_session, getLogger
from src.utils.filestore import (
    FileType,
    download_object,
    remove_from_filestore,
    upload_to_filestore,
)
from src.utils.responses import (
    BadRequestResponse,
    NotFoundResponse,
    SelfDestructFileResponse,
)

from .helpers import normalize_str

_log = getLogger(__name__)

router_v1 = APIRouter(prefix="/v1/ingredients", tags=[_tags.V1, _tags.Ingredient])


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


@router_v1.post("", response_model=IngredientPublic, status_code=201)
async def create_an_ingredient(
    ingredient: IngredientCreate = Depends(),
    file: UploadFile = File(None),
    session: Session = Depends(get_session),
):
    _log.debug("Creating a ingredient...")

    db_ingredient = Ingredient.model_validate(ingredient)
    if file and (f := file.file):
        assert (filename := file.filename)
        _log.debug(f"storing image with {filename = }")
        upload_to_filestore(f, filename, FileType.JPEG)
        db_ingredient.object_name = filename

    _log.debug(f"normalizing name {db_ingredient.name!r}")
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
            f, media_type="image/png", background_tasks=background_tasks
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
    if object_name := ingredient_db.object_name:
        _log.debug(f"deleting {object_name} from the filestore")
        remove_from_filestore(object_name)

        _log.debug("updating ingredients that were using the object image")
        q = (
            update(Ingredient)
            .where(Ingredient.object_name == object_name)  # type: ignore
            .values(object_name=None)
        )
        session.execute(q)
    session.delete(ingredient_db)
    session.commit()
    return {"ok": True}
