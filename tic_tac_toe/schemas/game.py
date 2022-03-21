from typing import List, Optional

from camel_converter.pydantic_base import CamelBase
from pydantic import validator


class Game(CamelBase):
    id: int
    board: List[List[str]] = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
    winner: Optional[str] = None

    class Config:
        orm_mode = True


class GameMove(CamelBase):
    game_id: int
    row: int
    col: int

    @validator("row")
    def validate_row_positiion(cls, v: int) -> int:
        if v < 0 or v > 2:
            raise ValueError(f"Row value must be between 0 and 2. {v} was sent.")

        return v

    @validator("col")
    def validate_col_positiion(cls, v: int) -> int:
        if v < 0 or v > 2:
            raise ValueError(f"Col value must be between 0 and 2. {v} was sent.")

        return v
