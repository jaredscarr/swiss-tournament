from pydantic import BaseSettings, PostgresDsn, validator
from typing import Any, Dict, Optional


class Settings(BaseSettings):
    APP_NAME: str = 'Swiss Tournament API'

    SECRET_KEY: str
    ALGORITHM: str
    TOKEN_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    # String of comma separated values
    CORS_ORIGINS: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:

        env_file = '.env'


settings = Settings()
