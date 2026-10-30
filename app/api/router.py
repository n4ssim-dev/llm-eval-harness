from fastapi import APIRouter

from app.api.routes import inference, logging, scoring

api_router = APIRouter()
api_router.include_router(inference.router)
api_router.include_router(scoring.router)
api_router.include_router(logging.router)
