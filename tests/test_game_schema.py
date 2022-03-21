import pytest

from tic_tac_toe.schemas.game import GameMove


def test_valid_move():
    move = GameMove(game_id=0, row=0, col=0)
    assert move.row == 0
    assert move.col == 0


@pytest.mark.parametrize("row", [-1, 3])
def test_invalid_row(row):
    with pytest.raises(ValueError):
        GameMove(game_id=0, row=row, col=0)


@pytest.mark.parametrize("col", [-1, 3])
def test_invalid_col(col):
    with pytest.raises(ValueError):
        GameMove(game_id=0, row=0, col=col)
