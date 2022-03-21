from sqlalchemy import Column, Integer, String

from tic_tac_toe.db.db import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    board = Column(String)
    winner = Column(String)
