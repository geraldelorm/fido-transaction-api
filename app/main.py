from fastapi import FastAPI
from app.api.routes import router as base_router
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
from app.config.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION

app = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

# Register exception handlers
app.add_exception_handler(ServiceError, service_error_handler)
app.add_exception_handler(EntityDoesNotExistError, entity_does_not_exist_error_handler)
app.add_exception_handler(EntityAlreadyExistsError, entity_already_exists_error_handler)
app.add_exception_handler(InvalidOperationError, invalid_operation_error_handler)

app.include_router(base_router.base_router, prefix=API_PREFIX, tags=["transactions"])