from typing import Dict, List

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from tic_tac_toe.crud.game import create_game, delete_game, get_all_games, get_game, update_game
from tic_tac_toe.db.db import get_db
from tic_tac_toe.errors import InvalidMoveError
from tic_tac_toe.game.game_controller import GameController, Player
from tic_tac_toe.schemas.game import Game, GameMove

router = APIRouter()


@router.get("/create", response_model=Game)
def create_game_route(db: Session = Depends(get_db)) -> Game:
    game = create_game(db)

    if not game:
        raise HTTPException(status_code=400, detail="Error creating game")

    return game


@router.delete("/{id}", status_code=202)
def delete_game_route(id: int, db: Session = Depends(get_db)) -> Dict[str, str]:
    result = delete_game(id, db)

    if result < 1:
        raise HTTPException(400, detail="No records deleted")

    return {"msg": "Record successfully deleted"}


@router.get("/all", response_model=List[Game])
def get_all_games_route(db: Session = Depends(get_db)) -> List[Game]:
    games = get_all_games(db)
    if not games:
        raise HTTPException(status_code=404, detail="No games found")

    return games


@router.get("/{id}", response_model=Game)
def get_game_route(id: int, db: Session = Depends(get_db)) -> Game:
    game = get_game(id, db)

    if not game:
        raise HTTPException(status_code=404, detail=f"Game {id} not found")

    return game


@router.post("/move", response_model=Game)
def make_move(move: GameMove, db: Session = Depends(get_db)) -> Game:
    game = get_game(move.game_id, db)
    if not game:
        raise HTTPException(status_code=404, detail=f"Game {move.game_id} not found")

    if game.winner:
        raise HTTPException(
            status_code=400, detail=f"Game is completed. The winner was {game.winner}"
        )

    game_controler = GameController(board=game.board, winner=game.winner)

    try:
        game_controler.move(Player.PLAYER_X, (move.row, move.col))
    except InvalidMoveError:
        raise HTTPException(
            status_code=400, detail=f"Not a valid move. Current board: {game.board}"
        )

    updated_game = update_game(
        Game(id=game.id, board=game_controler.board, winner=game_controler.winner), db
    )

    if game_controler.winner and updated_game:
        return updated_game

    game_controler.move(Player.PLAYER_O)
    updated_game = update_game(
        Game(id=game.id, board=game_controler.board, winner=game_controler.winner), db
    )

    if game_controler.winner and updated_game:
        return updated_game

    if updated_game:
        return updated_game

    return game
