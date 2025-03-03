from fastapi import APIRouter
from .endpoints import process, youtube, dashboard, auth

api_router = APIRouter(prefix="/api")

# Include routers from endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(process.router, prefix="/process", tags=["process"])
api_router.include_router(youtube.router, prefix="/youtube", tags=["youtube"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"]) 