from fastapi import APIRouter

from src.api.routes import auth, spots, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(spots.router, prefix="/spots", tags=["spots"])
