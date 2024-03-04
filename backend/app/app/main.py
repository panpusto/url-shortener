from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.db.init_db import init_db
from app.api.api_v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    lifespan=lifespan
)

app.include_router(api_router)
