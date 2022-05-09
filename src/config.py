import logging
from typing import Any, Dict, Optional

import dotenv
from pydantic import BaseSettings, validator

dotenv.load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = 'Test First VDS'

    HOST: str = '127.0.0.1'
    PORT: int = 8000

    LOG_LEVEL: int = logging.INFO

    MONGODB_HOST: str = 'db'
    MONGODB_DB: str = 'test_first_vds'

    MONGODB_URL: str = None

    @validator('MONGODB_URL', pre=True)
    def assemble_db_connection(cls, value: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(value, str):
            return value

        return f"mongodb://" \
               f"{values.get('MONGODB_HOST')}/" \
               f"{values.get('MONGODB_DB')}?" \
               f"retryWrites=true&w=majority"

    CELERY_BROKER_URL: str = "redis://localhost:6379"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379"

    class Config:
        case_sensitive = True
        env_file = "../.env"
        env_file_encoding = "utf-8"


settings = Settings()
