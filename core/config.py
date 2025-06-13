from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Literal

class Settings(BaseSettings):
    MODE: Literal["dev", "prod", "test"] = "dev"  # Added "test" to allowed values

    PROJECT_NAME: str = "Travel Wallet"
    DATABASE_URL: str
    SECRET_KEY: str = "huaoibdusyia1535"

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

# Function to clear the cache during testing
def clear_settings_cache():
    """Clear the settings cache. Useful for testing."""
    get_settings.cache_clear()

settings = get_settings()