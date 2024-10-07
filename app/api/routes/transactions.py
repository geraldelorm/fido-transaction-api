from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from loguru import logger

from app.crud.transactions_service import (
    add_transaction,
    delete_transaction,
    retrieve_transaction,
    retrieve_transaction_history,
    update_transaction,
)
from app.exceptions.exceptions import ServiceError, EntityDoesNotExistError
from app.models.transaction_model import (
    TransactionModel,
    UpdateTransactionModel,
    ResponseModel,
)

router = APIRouter()

@router.post(
    "/",
    response_description="New Transaction record added",
    response_model=ResponseModel,
    status_code=status.HTTP_201_CREATED,
)
async def add_transaction_record(transaction: TransactionModel = Body(...)):
    logger.info("Adding a transaction record")
    transaction = jsonable_encoder(transaction)
    try:
        new_transaction = await add_transaction(transaction)
        logger.info("Added a transaction record")
        return ResponseModel(
            new_transaction, "Transaction added successfully.", status.HTTP_201_CREATED
        )
    except Exception as e:
        logger.error("An error occurred while adding a transaction record", e)
        raise ServiceError()


@router.get(
    "/{id}",
    response_description="Transaction data retrieved",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
)
async def get_transaction_data(id: str):
    logger.info(f"Retrieving transaction data for ID: {id}")
    try:
        transaction = await retrieve_transaction(id)
        return ResponseModel(
            transaction, "Transaction data retrieved successfully", status.HTTP_200_OK
        )
    except EntityDoesNotExistError as e:
        logger.error(f"Transaction not found for ID: {id}")
        raise EntityDoesNotExistError(f"Transaction with id: {id} not found.")
    except Exception as e:
        logger.error(
            f"An error occurred while retrieving transaction data for ID: {id}", e
        )
        raise ServiceError("An error occurred while retrieving transaction data")


@router.get(
    "/history/{user_id}",
    response_description="User transaction history retrieved",
    response_model=ResponseModel,
)
async def get_transaction_history(user_id: str):
    logger.info(f"Retrieving transaction history for user ID: {user_id}")
    try:
        transaction_history = await retrieve_transaction_history(user_id)
        logger.info(f"Transaction history retrieved for user ID: {user_id}")
        return ResponseModel(
            transaction_history,
            "Transaction history retrieved successfully",
            status.HTTP_200_OK,
        )
    except EntityDoesNotExistError as e:
        logger.error(f"Transaction history not found for user ID: {user_id}")
        raise EntityDoesNotExistError(
            f"Transaction history not found for user ID {user_id}"
        )
    except Exception as e:
        logger.error(
            f"An error occurred while retrieving transaction history for user ID: {user_id}",
            e,
        )
        raise ServiceError()


@router.put(
    "/{id}",
    response_description="Transaction data updated",
    response_model=ResponseModel,
)
async def update_transaction_data(id: str, req: UpdateTransactionModel = Body(...)):
    logger.info(f"Updating transaction data for ID: {id}")
    req = {k: v for k, v in req.dict().items() if v is not None}
    try:
        updated_transaction = await update_transaction(id, req)
        if updated_transaction:
            logger.info(f"Transaction with ID: {id} updated")
            return ResponseModel(
                f"Transaction with ID: {id} update is successful",
                "Transaction updated successfully",
                status.HTTP_200_OK,
            )
        else:
            logger.warning(f"Transaction with ID: {id} not found")
            raise EntityDoesNotExistError(f"Transaction with id: {id} not found.")
    except EntityDoesNotExistError as e:
        logger.error(f"Transaction not found for ID: {id}")
        raise EntityDoesNotExistError(f"Transaction not found for ID: {id}")
    except Exception as e:
        raise ServiceError()


@router.delete(
    "/{id}",
    response_description="Transaction data deleted from the database",
    response_model=ResponseModel,
)
async def delete_transaction_data(id: str):
    logger.info(f"Deleting transaction data for ID: {id}")
    try:
        deleted_transaction = await delete_transaction(id)
        if deleted_transaction:
            logger.info(f"Transaction with ID: {id} deleted")
            return ResponseModel(
                f"Transaction with ID: {id} removed",
                "Transaction deleted successfully",
                status.HTTP_200_OK,
            )
        else:
            logger.warning(f"Transaction with ID: {id} not found")
            raise EntityDoesNotExistError(f"Transaction with id: {id} not found.")
    except EntityDoesNotExistError as e:
        logger.error(f"Transaction not found for ID: {id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(
            f"An error occurred while deleting transaction data for ID: {id}",
            exc_info=True,
        )
        raise ServiceError()
