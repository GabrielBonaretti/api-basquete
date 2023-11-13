from fastapi import APIRouter
from api.v1.endpoints import league
from api.v1.endpoints import teams

api_router = APIRouter()

api_router.include_router(league.router, prefix='/leagues', tags= ["leagues"])
api_router.include_router(teams.router, prefix='/teams', tags= ["teams"])