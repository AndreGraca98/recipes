from fastapi import APIRouter

from src.routers import _tags
from src.utils import getLogger
from src.utils.filestore import (
    FileStore,
    FilestoreObject,
)

_log = getLogger(__name__)

router_v1 = APIRouter(prefix="/v1/filestore-objects", tags=[_tags.V1, _tags.Filestore])


@router_v1.get("", response_model=list[FilestoreObject])
async def get_filestore_objects():
    filestore = FileStore()
    return list(filestore.list_objects())


@router_v1.get("/exists")
async def does_filestore_object_exist(object_name: str):
    filestore = FileStore()
    return {"exists": filestore.object_exists(object_name)}


@router_v1.delete("")
async def remove_filestore_object(object_name: str):
    filestore = FileStore()
    filestore.remove_object(object_name)
    return {"ok": True}
