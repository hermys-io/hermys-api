from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    # Environment
    ENVIRONMENT: str = 'local'

    # Mongo
    MONGODB_URI: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str

    # CORS settings
    ALLOWED_ORIGINS: str

    # Scout APM
    SCOUT_KEY: str

    # B2
    B2_BUCKET_NAME: str
    B2_APPLICATION_KEY_ID: str
    B2_APPLICATION_KEY: str

    # Pinecone
    PINECONE_API_KEY: str
    PINECONE_CLOUD: str
    PINECONE_REGION: str

    # OpenAI
    OPENAI_API_KEY: str

    # LangChain
    LANGCHAIN_API_KEY: str

    # Sentry
    SENTRY_DNS: str


@cache
def get_settings():
    return Settings()  # type: ignore
