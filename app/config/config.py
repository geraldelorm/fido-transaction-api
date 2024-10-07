import sys
import logging

from loguru import logger
from starlette.config import Config
from starlette.datastructures import Secret

from app.config.logging import InterceptHandler

config = Config(".env")

API_PREFIX = "/api"
VERSION = "0.1.0"
DEBUG: bool = config("DEBUG", cast=bool, default=False)
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret, default="")

PROJECT_NAME: str = config("PROJECT_NAME", default="fido-transactions-api")
MONGO_URI: str = config("MONGO_URI", default="mongodb://localhost:27017/")
MONGO_DB_NAME: str = config("MONGO_DB_NAME", default="fido_transactions_db")
FIDO_TRANSACTIONS_COLLECTION: str = config("FIDO_TRANSACTIONS_COLLECTION", default="transactions")

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
