import logging

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from src.routers import ROUTERS, TAGS_METADATA

from .utils import Environment, getLogger
from .utils.responses import ExceptionJSONResponse

_log = getLogger(__name__)

_log.log(
    logging.getLevelNamesMapping()[Environment().LOG_LEVEL],
    f"Starting API in {Environment().LOG_LEVEL} mode...",
)

swagger_ui_parameters = {
    "defaultModelsExpandDepth": -1,  # Hide models section by default
    "docExpansion": "none",  # Collapse all sections by default
}
api = FastAPI(
    title="API",
    swagger_ui_parameters=swagger_ui_parameters,
    openapi_tags=TAGS_METADATA,
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
    except Exception as e:
        _log.exception(str(e))
        return ExceptionJSONResponse(status_code=500, error=e, error_details=ctx)


# Include all routers in the APP
for router in ROUTERS:
    api.include_router(router)


@api.get("/", include_in_schema=False)
async def homepage():
    return RedirectResponse(url="/public/index.html")


@api.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse(url="/public/favicon.ico")
