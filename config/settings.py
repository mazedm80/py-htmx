from pydantic_settings import BaseSettings


class ApiSettings(BaseSettings):
    """Schema for configuring API parameters."""

    host: str = "localhost"
    port: int = 3000
    debug: bool = False
    workers: int = 1
    api_host: str = "http://localhost:5000"
    # api_host: str = "https://htmx.euro-bangla.eu"

    class Config:
        env_prefix = "API_"
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = ApiSettings()
