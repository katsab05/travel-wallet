from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env into environment variables

class Settings:
    PROJECT_NAME = "Travel Wallet"
    DATABASE_URL = os.getenv("DATABASE_URL")

settings = Settings()
