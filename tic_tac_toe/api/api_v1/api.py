from fastapi import APIRouter

from tic_tac_toe.api.api_v1.endpoints import game

api_router = APIRouter()
api_router.include_router(game.router, prefix="/game", tags=["game"])
