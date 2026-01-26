from typing import Optional

from pydantic import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENV_STAT: Optional[str] = None

    class Config:
        env_file = ".env"

class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False

class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_")

class TestConfig(GlobalConfig):
    
    DATABASE_URL = "sqlite:///./test.db"
    DB_FORCE_ROLL_BACK = True

class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_")
        