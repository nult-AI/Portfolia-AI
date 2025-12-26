from fastapi import APIRouter
from app.api.v1.endpoints import portfolio, cv

api_router = APIRouter()
api_router.include_router(portfolio.router, tags=["portfolio"])
api_router.include_router(cv.router, prefix="/cv", tags=["cv extraction"])
