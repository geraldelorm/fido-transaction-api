from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.exceptions import (
    ServiceError,
    EntityDoesNotExistError,
    EntityAlreadyExistsError,
    InvalidOperationError,
)


async def service_error_handler(request: Request, exc: ServiceError):
    return JSONResponse(
        status_code=503,
        content={"message": exc.message, "name": exc.name},
    )


async def entity_does_not_exist_error_handler(
    request: Request, exc: EntityDoesNotExistError
):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message, "name": exc.name},
    )


async def entity_already_exists_error_handler(
    request: Request, exc: EntityAlreadyExistsError
):
    return JSONResponse(
        status_code=409,
        content={"message": exc.message, "name": exc.name},
    )


async def invalid_operation_error_handler(request: Request, exc: InvalidOperationError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message, "name": exc.name},
    )
