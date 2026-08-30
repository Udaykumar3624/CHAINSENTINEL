import os
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "ChainSentinel"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/chainsentinel"

    # CORS settings
    CORS_ORIGINS: Union[str, List[str]] = "http://localhost:5173,http://127.0.0.1:5173"

    @field_validator("CORS_ORIGINS", mode="before")
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    # Security and Auth settings
    JWT_SECRET_KEY: str = "chainsentinel-sih26146-super-secret-jwt-key-2026"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 600

    # Seeded Demo Investigator Account
    DEMO_USERNAME: str = "demo.investigator"
    DEMO_PASSWORD: str = "Investigator2026!"
    DEMO_EMAIL: str = "demo@chainsentinel.local"
    DEMO_FULL_NAME: str = "Lead Investigator"

    # External Provider Configuration
    LIVE_DATA_ENABLED: bool = False
    MEMPOOL_API_URL: str = "https://mempool.space/api"
    REQUEST_TIMEOUT_SECONDS: int = 10

    # Safety and Graph limits
    MAX_GRAPH_NODES: int = 150
    MAX_UPLOAD_ROWS: int = 10000

    # UI & API docs
    ENABLE_DOCS: bool = True

    @field_validator("ENABLE_DOCS", mode="before")
    def set_docs_visibility(cls, v: Union[bool, str], info) -> bool:
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes")
        return v

    # Machine Learning configuration
    MODEL_PATH: str = "app/ml/models/risk_model.joblib"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
