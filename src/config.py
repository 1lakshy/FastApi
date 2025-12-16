from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    database_url: str

    model_config = ConfigDict(
        env_file = ".env",
        extra = "ignore"
    )


Config = Settings()