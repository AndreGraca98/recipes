from fastapi import APIRouter

from src.utils import getLogger

from .. import _tags

_log = getLogger(__name__)

router_v1 = APIRouter(prefix="/v1/ingredients", tags=[_tags.V1, _tags.Ingredient])


# @router_v1.get("/total-price")
# async def get_total_price(session: SessionDependency):
#     q = select((Ingredient.name))
#     total_price = session.scalar(q)
#     return total_price
