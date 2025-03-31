from fastapi import APIRouter
from sqlmodel import select

from src.models import Recipe
from src.utils import getLogger
from src.utils.session import SessionDependency

from .. import _tags

_log = getLogger(__name__)

router_v1 = APIRouter(prefix="/v1/recipes", tags=[_tags.V1, _tags.Recipe])


@router_v1.post("")
async def create_a_new_recipe(session: SessionDependency):
    select((Recipe))
    return {"foo": "bar"}
