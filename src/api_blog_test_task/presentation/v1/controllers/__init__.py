from fastapi import FastAPI, APIRouter

from .posts import posts_router

def setup_controllers(app: FastAPI, *routers: APIRouter) -> None:
    v1_router = APIRouter()

    for router in routers:
        v1_router.include_router(router)

    app.include_router(v1_router)


__all__ = (
    "posts_router",
    "setup_controllers",
)
