import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from points.base import router as points_router, router_lifespan as points_lifespan
from common.base import router as common_router
from global_variables import global_variables

logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format="%(asctime)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    # SINGLE APPLICATIONS STARTUP
    await points_lifespan[0](fastapi_app)

    # MAIN APPLICATION STARTUP
    global_variables.APP = fastapi_app
    yield

    # SINGLE APPLICATIONS SHUTDOWN
    await points_lifespan[1](fastapi_app)


app = FastAPI(lifespan=lifespan)


origins = [
    "*",  # replace with your frontend domain
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # specify allowed HTTP methods
    allow_headers=["*"],  # allow all headers, adjust as needed
    expose_headers=["Content-Disposition"],  # expose specific headers, if required
)

app.include_router(common_router)
app.include_router(points_router)
