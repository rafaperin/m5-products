import pathlib
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class MongoDBSettings(BaseSettings):
    MONGO_DATABASE: str
    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    MONGO_HOST: str

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


class Settings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str

    ENVIRONMENT: str

    db: MongoDBSettings = MongoDBSettings()

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
