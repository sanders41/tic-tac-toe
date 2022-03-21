import asyncio
from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tic_tac_toe.core.config import settings
from tic_tac_toe.db.db import Base, get_db
from tic_tac_toe.main import app

ROOT_PATH = Path().absolute()
_DB_NAME = "test_game.db"
_ENGINE = create_engine(f"sqlite:///{_DB_NAME}")
_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_ENGINE)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(_ENGINE)
    yield
    db_file = ROOT_PATH / _DB_NAME
    db_file.unlink()


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


def mock_db():
    db = _SessionLocal()
    yield db
    db.close()


@pytest.fixture(autouse=True)
def mock_get_db():
    app.dependency_overrides[get_db] = mock_db


@pytest.fixture
async def test_client():
    async with AsyncClient(app=app, base_url=f"http://localhost{settings.API_V1_STR}") as ac:
        yield ac
