from pydantic_settings import BaseSettings
from enum import Enum 
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGODB_URL = os.getenv('MONGODB_URL')

SECRET_KEY = "4f400364dc36a8bd1895874efe0b7469f29e7ed863ec903c5f10d8e82dc7c4d9"
REFRESH_SECRET_KEY="2bbed1f1b49f306ca855027cd0a94c421805c91a244d6cb75298c4c850e0f8cf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24*1 #( 1 days )
REFRESH_TOKEN_EXPIRE_DAYS = 7 #( days )

class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True


class Config(BaseConfig):
    DEBUG: int = 0
    DEFAULT_LOCALE: str = "en_US"
    ENVIRONMENT: str = EnvironmentType.DEVELOPMENT
    # REDIS_URL: RedisDsn = "redis://localhost:6379/7"
    RELEASE_VERSION: str = "0.1"
    SHOW_SQL_ALCHEMY_QUERIES: int = 0
    SECRET_KEY: str = SECRET_KEY
    ALGORITHM: str = ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES: int = ACCESS_TOKEN_EXPIRE_MINUTES
    # CELERY_BROKER_URL: str = "amqp://rabbit:password@localhost:5672"
    # CELERY_BACKEND_URL: str = "redis://localhost:6379/0"


config: Config = Config()
