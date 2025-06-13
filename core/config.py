from pydantic import BaseSettings
from functools import lru_cache
from typing import Literal

class Settings(BaseSettings):
    MODE: Literal["dev", "prod"] = "dev"

    PROJECT_NAME: str = "Travel Wallet"
    DATABASE_URL: str

    # S3 settings 
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_BUCKET_NAME: str = ""
    AWS_REGION: str = ""

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
