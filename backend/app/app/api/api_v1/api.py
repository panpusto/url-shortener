from fastapi import APIRouter

from .endpoints import urls


api_router = APIRouter()
api_router.include_router(urls.router, tags=["urls"])
