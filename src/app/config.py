from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "change-me-in-production"
    REDIS_URL: str = "redis://localhost:6379"

    model_config = {"env_file": ".env"}


settings = Settings()
