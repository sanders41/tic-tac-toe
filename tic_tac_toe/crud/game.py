from __future__ import annotations

from sqlalchemy.orm import Session

from tic_tac_toe.core.board import DEFAULT_BOARD
from tic_tac_toe.db import models
from tic_tac_toe.schemas.game import Game
from tic_tac_toe.utils.converters import str_to_board


def create_game(db: Session) -> Game | None:
    game = models.Game(board=str(DEFAULT_BOARD), winner=None)
    db.add(game)
    db.commit()
    db.refresh(game)
    new_game = get_game(game.id, db)

    if not new_game:
        return None

    return Game(id=new_game.id, board=new_game.board, winner=new_game.winner)


def delete_game(id: int, db: Session) -> int:
    result = db.query(models.Game).where(models.Game.id == id).delete()
    db.commit()
    return result


def get_all_games(db: Session) -> list[Game] | None:
    games = db.query(models.Game).all()

    if not games:
        return None

    return [Game(id=x.id, board=str_to_board(x.board), winner=x.winner) for x in games]


def get_game(id: int, db: Session) -> Game | None:
    game = db.query(models.Game).filter(models.Game.id == id).first()

    if not game:
        return None

    return Game(id=game.id, board=str_to_board(game.board), winner=game.winner)


def update_game(game: Game, db: Session) -> Game | None:
    db.query(models.Game).where(models.Game.id == game.id).update(
        {"board": str(game.board), "winner": game.winner}
    )
    db.commit()

    updated_game = get_game(game.id, db)

    if not updated_game:
        return None

    return updated_game
