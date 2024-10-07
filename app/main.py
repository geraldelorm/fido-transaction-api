from fastapi import FastAPI
from loguru import logger
from app.api.routes.router import base_router
from app.config.config import (
    API_PREFIX,
    DEBUG,
    PROJECT_NAME,
    VERSION,
    MONGODB_URI,
    MONGO_DB_NAME,
)
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from app.exceptions.exception_handler import (
    service_error_handler,
    entity_does_not_exist_error_handler,
    entity_already_exists_error_handler,
    invalid_operation_error_handler,
)
from app.exceptions.exceptions import (
    ServiceError,
    EntityDoesNotExistError,
    EntityAlreadyExistsError,
    InvalidOperationError,
)

app = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

client = AsyncIOMotorClient(MONGODB_URI)
database = client[MONGO_DB_NAME]


# Establishing a connection to MongoDB
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await database.command("ping")
        logger.info(MONGODB_URI)
        logger.info("Successfully connected to MongoDB")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise ServiceError("MongoDB connection error")
    yield

    await client.close()


app = FastAPI(lifespan=lifespan)


@app.get("/", tags=["root-ping"])
async def root():
    return {"message": "Welcome to Fido Transactions API"}


# Registering exception handlers
app.add_exception_handler(ServiceError, service_error_handler)
app.add_exception_handler(EntityDoesNotExistError, entity_does_not_exist_error_handler)
app.add_exception_handler(EntityAlreadyExistsError, entity_already_exists_error_handler)
app.add_exception_handler(InvalidOperationError, invalid_operation_error_handler)

app.include_router(base_router, prefix=API_PREFIX, tags=["transactions"])
