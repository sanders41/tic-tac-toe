from __future__ import annotations


def str_to_board(string_board: str) -> list[list[str]]:
    board_splits = string_board[2:-2].strip().split("[")
    board = []

    for board_split in board_splits:
        board.append(board_split.strip().replace(",", "").replace("'", "").replace("]", "").split())

    return board
