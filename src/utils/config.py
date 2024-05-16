import os
from dataclasses import Field

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "XiW5JX9LURpyjuIPP9fDS-_ncYhfNWuAGdcnebEa_nM"
    LOG_DATE_FMT: str = "%Y-%m-%dT%H:%M:%S"
    LOG_FORMAT: str = "%(asctime)s %(levelname)s [%(pathname)s:%(lineno)d] [%(email)s: %(request_id)s] %(message)s"

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    PG_HOST: str
    PG_USER: str
    PG_PASSWORD: str
    DB_NAME: str
    DEPLOYMENT_TYPE: str


settings = Settings()
