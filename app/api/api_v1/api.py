from fastapi import APIRouter

from .routes import competitors, matches, tournaments, users

api_router = APIRouter()
api_router.include_router(
    competitors.router,
    prefix='/swiss-tournament',
    tags=['swiss-api']
)
api_router.include_router(
    matches.router,
    prefix='/swiss-tournament',
    tags=['swiss-api']
)
api_router.include_router(
    tournaments.router,
    prefix='/swiss-tournament',
    tags=['swiss-api']
)
api_router.include_router(
    users.router,
    prefix='/swiss-tournament',
    tags=['swiss-api']
)