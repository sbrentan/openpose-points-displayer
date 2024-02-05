from typing import Callable, Tuple

from fastapi import APIRouter

from points.database.database import points_database
from points.routers.document.document import router as document_router
from global_variables import global_variables

router = APIRouter(
    prefix="/points",
    tags=["points"]
)


async def router_startup(fastapi_app):
    print("Starting up the points...")
    global_variables.databases["points"] = points_database


async def router_shutdown(fastapi_app):
    print("Shutting down the points...")

router_lifespan: Tuple[Callable, Callable] = (router_startup, router_shutdown)


router.include_router(document_router)
