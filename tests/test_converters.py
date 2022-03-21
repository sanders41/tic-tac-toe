from tic_tac_toe.core.board import DEFAULT_BOARD
from tic_tac_toe.utils.converters import str_to_board


def test_str_to_board():
    result = str_to_board(str(DEFAULT_BOARD))
    assert result == DEFAULT_BOARD
