from copy import deepcopy

import pytest

from tic_tac_toe.errors import InvalidMoveError
from tic_tac_toe.game.game_controller import GameController, NoMovesAvailableError, Player


@pytest.mark.parametrize(
    "board",
    [
        [["X", "X", "X"], ["O", "O", "."], ["O", ".", "."]],
        [["O", "O", "."], ["X", "X", "X"], ["O", ".", "."]],
        [[".", ".", "."], ["O", "O", "."], ["X", "X", "X"]],
        [["X", "O", "O"], ["X", "O", "."], ["X", ".", "."]],
        [[".", "X", "O"], ["O", "X", "."], ["O", "X", "."]],
        [[".", ".", "X"], [".", "O", "X"], [".", "O", "X"]],
        [["X", "O", "."], ["O", "X", "."], ["O", ".", "X"]],
        [[".", "O", "X"], ["O", "X", "."], ["X", ".", "."]],
    ],
)
def test_check_winner(board):
    game = GameController()
    game.board = board
    game.check_winner()

    assert game.winner == "X"


def test_check_no_winner():
    game = GameController()
    game.board = [["X", "O", "X"], ["X", "O", "X"], ["O", "X", "O"]]
    game.check_winner()

    assert game.winner is None


@pytest.mark.parametrize(
    "board, available",
    [
        ([["X", "O", "X"], ["O", "X", "O"], ["X", "O", "."]], [(2, 2)]),
        ([[".", "O", "X"], ["O", "X", "O"], ["X", "O", "."]], [(0, 0), (2, 2)]),
    ],
)
def test_available_spots(board, available):
    game = GameController()
    game.board = board

    assert game.available_spots() == available


def test_available_spots_none():
    game = GameController()
    game.board = [["X", "O", "X"], ["X", "O", "X"], ["O", "X", "O"]]

    with pytest.raises(NoMovesAvailableError):
        game.available_spots()


def test_move_with_position():
    game = GameController()
    game.board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
    game.move(Player.PLAYER_X, (1, 1))

    assert game.board == [[".", ".", "."], [".", "X", "."], [".", ".", "."]]


def test_move_with_no_position():
    game = GameController()
    board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
    game.board = deepcopy(board)
    game.move(Player.PLAYER_X)

    assert game.board != board


def test_random_move():
    game = GameController()
    move = game.random_move()
    assert -1 < move[0] < 3
    assert -1 < move[1] < 3


def test_draw():
    game = GameController()
    game.board = [["X", "O", "X"], ["X", "O", "X"], ["O", "X", "O"]]
    game.move(Player.PLAYER_X)
    assert "draw" in game.winner  # type: ignore


def test_spot_taken():
    game = GameController()
    game.board = [["X", "O", "X"], ["X", "O", "."], ["O", "X", "O"]]
    with pytest.raises(InvalidMoveError):
        game.move(Player.PLAYER_X, (0, 0))
