from __future__ import annotations

import os

from pydantic.v1 import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Book Management API"

    DATABASE_URL = (
        f"postgresql+asyncpg://{os.getenv('pg_user')}:{os.getenv('pg_password')}"
        f"@{os.getenv('pg_host')}/{os.getenv('pg_db_name')}"
    )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
