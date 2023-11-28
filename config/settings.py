from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class API(BaseModel):
    """Schema for configuring API parameters."""

    host: str = "localhost"
    port: int = 3000
    debug: bool = False
    workers: int = 1
    api_host: str = ""
    # api_host: str = "https://htmx.euro-bangla.eu"


class Settings(BaseSettings):
    """Schema for configuring API parameters."""

    api: API = API()

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
