from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    # Mongo
    MONGODB_URI: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str

    # CORS settings
    ALLOWED_ORIGINS: str

    # Scout APM
    SCOUT_KEY: str


@cache
def get_settings():
    return Settings()  # type: ignore
