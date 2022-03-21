from __future__ import annotations

from enum import Enum
from random import randint

from tic_tac_toe.core.board import DEFAULT_BOARD
from tic_tac_toe.errors import InvalidMoveError, NoMovesAvailableError


class Player(Enum):
    PLAYER_X = "X"
    PLAYER_O = "O"


class GameController:
    def __init__(
        self,
        board: list[list[str]] = DEFAULT_BOARD,
        winner: str | None = None,
    ) -> None:
        self.board = board
        self.winner = winner

    def available_spots(self) -> list[tuple[int, int]]:
        available = []
        for i, row in enumerate(self.board):
            for j, column in enumerate(row):
                if column == ".":
                    available.append((i, j))

        if not available:
            raise NoMovesAvailableError("It's a draw")

        return available

    def check_winner(self) -> None:
        # Check for across winner
        for i, row in enumerate(self.board):
            across_set = set(row)
            if len(across_set) == 1 and list(across_set)[0] != ".":
                self.winner = list(across_set)[0]
                return None

        # Check for down winner
        for i in range(3):
            if self.board[0][i] != ".":
                if self.board[0][i] == self.board[1][i] == self.board[2][i]:
                    self.winner = self.board[0][i]
                    return None

        # Check for diagnal winner
        if self.board[0][0] != ".":
            if self.board[0][0] == self.board[1][1] == self.board[2][2]:
                self.winner = self.board[0][0]
                return None
        if self.board[0][2] != ".":
            if self.board[0][2] == self.board[1][1] == self.board[2][0]:
                self.winner = self.board[0][2]
                return None

    def move(self, player: Player, position: tuple[int, int] | None = None) -> None:
        try:
            self.available_spots()
        except NoMovesAvailableError:
            self.check_winner()
            if not self.winner:
                self.winner = "It's a draw"

            return None

        if position:
            if not self._is_valid_move(position):
                raise InvalidMoveError("Spot is already taken")

            move = position
        else:
            move = self.random_move()

        self.board[move[0]][move[1]] = player.value
        self.check_winner()

    def random_move(self) -> tuple[int, int]:
        available_spots = self.available_spots()
        move = randint(0, len(available_spots) - 1)
        return available_spots[move]

    def _is_valid_move(self, position: tuple[int, int]) -> bool:
        if (
            position not in self.available_spots()
            or position[0] < 0
            or position[0] > 2
            or position[1] < 0
            or position[1] > 2
        ):
            return False

        return True
