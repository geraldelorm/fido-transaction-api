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

MONGODB_URI: str = config("MONGODB_URI", default="mongodb://mongodb:27017/")
MONGO_DB_NAME: str = config("MONGO_DB_NAME", default="fido_transactions_db")
MONGO_INITDB_ROOT_USERNAME: str = config("MONGO_INITDB_ROOT_USERNAME", default="myuser")
MONGO_INITDB_ROOT_PASSWORD: str = config("MONGO_INITDB_ROOT_USERNAME", default="mypass")
FIDO_TRANSACTIONS_COLLECTION: str = config(
    "FIDO_TRANSACTIONS_COLLECTION", default="transactions"
)

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
