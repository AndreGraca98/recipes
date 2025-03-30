import logging
from contextlib import asynccontextmanager

import sqlalchemy
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel

from .routers import ROUTERS, TAGS_METADATA
from .utils import Environment, getLogger
from .utils.exception_handlers import handle_integrity_error
from .utils.responses import ServerExceptionResponse
from .utils.session import engine

_log = getLogger(__name__)

_log.log(
    logging.getLevelNamesMapping()[Environment().LOG_LEVEL],
    f"Starting API in {Environment().LOG_LEVEL} mode...",
)

swagger_ui_parameters = {
    "defaultModelsExpandDepth": -1,  # Hide models section by default
    "docExpansion": "none",  # Collapse all sections by default
}


# Create the SQLmodels
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


api = FastAPI(
    title="Recipes Manager API",
    swagger_ui_parameters=swagger_ui_parameters,
    openapi_tags=TAGS_METADATA,
    lifespan=lifespan,
)
"""The global FastAPI instance"""

# Serve the assets directory
api.mount("/public", StaticFiles(directory="public"))
api.mount("/assets", StaticFiles(directory="assets"))


# Middleware to handle exceptions and log them
@api.middleware("http")
async def exception_handling_middleware(request: Request, call_next):
    ctx = dict(
        request=dict(
            url=str(request.url),
            headers=dict(request.headers),
            query_params=dict(request.query_params),
            path_params=request.path_params,
        )
    )
    try:
        return await call_next(request)
    # except ... as e: # Add other exceptions here. using dataclasses can have custom
    # data passed to the error details
    #     ...
    except sqlalchemy.exc.IntegrityError as e:
        return handle_integrity_error(e, ctx)
    except Exception as e:
        # _log.exception(str(e))
        return ServerExceptionResponse(error=e, error_details=ctx)


# Include all routers in the APP
for router in ROUTERS:
    api.include_router(router)


@api.get("/", include_in_schema=False)
async def homepage():
    return RedirectResponse(url="/public/index.html")


@api.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse(url="/public/favicon.ico")
