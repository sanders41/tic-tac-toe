from fastapi import FastAPI

from tic_tac_toe.api.api_v1.api import api_router
from tic_tac_toe.core.config import settings
from tic_tac_toe.db.db import create_db

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")


@app.on_event("startup")
def startup_create_db() -> None:
    create_db()


app.include_router(api_router, prefix=settings.API_V1_STR)
