from functools import lru_cache
from typing import Any, Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    # APP
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    # CORS
    cors_origins: list[str] = ["*"]

    # Logging
    log_level: str = "WARNING"
    log_file_path: Optional[str] = None

    # Development
    dev_uvicorn_reload: bool = False

    class Config:
        env_file = ".env"

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if field_name == "cors_origins":
                return [item for item in raw_val.split(",")]
            return cls.json_loads(raw_val)  # type: ignore


@lru_cache(1)
def get_settings() -> Settings:
    return Settings()
