# config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database URL
    DATABASE_URL: str = "postgresql://postgres:amsa0406@localhost/myprojectdb"

    # JWT Settings
    # Generate a secret key with: openssl rand -hex 32
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"

settings = Settings()
