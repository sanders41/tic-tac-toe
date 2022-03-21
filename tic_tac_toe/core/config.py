from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Tic-Tac-Toe"
    API_V1_STR: str = "/api/v1"
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///game.db"

    class Config:
        case_sensitive = True


settings = Settings()
