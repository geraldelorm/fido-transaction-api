from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Query, status
from loguru import logger

from app.crud.analytics_service import retrieve_transaction_analytics, retrieve_live_transaction_analytics
from app.exceptions.exceptions import ServiceError, EntityDoesNotExistError
from app.models.analytics_model import ResponseModel

router = APIRouter()

@router.get(
    "/{user_id}",
    response_description="User analytics retrieved",
    response_model=ResponseModel,
)
async def get_transaction_analytics(user_id: str):
    logger.info(f"Retrieving transaction analytics for user ID: {user_id}")
    try:
        analytics = await retrieve_transaction_analytics(user_id)
        logger.info(f"Transaction analytics retrieved for user ID: {user_id}")
        return ResponseModel(
            analytics,
            "Transaction analytics retrieved successfully",
            status.HTTP_200_OK,
        )
    except EntityDoesNotExistError as e:
        logger.error(f"Transaction analytics not found for user ID: {user_id}")
        raise EntityDoesNotExistError(
            f"Transaction analytics not found for user ID {user_id}"
        )
    except Exception as e:
        logger.error(
            f"An error occurred while retrieving transaction analytics for user ID: {user_id}",
            e.with_traceback(),
        )
        raise ServiceError()


@router.get(
    "/range/{user_id}",
    response_description="User analytics retrieved for time period",
    response_model=ResponseModel,
)
async def get_range_transaction_analytics(
    user_id: str,
    start_date: Optional[datetime] = Query(None, description="Start date for the period e.g 2024-10-08T01:05:37.574299"),
    end_date: Optional[datetime] = Query(None, description="End date for the period e.g 2024-11-08T01:05:37.574299"),
):
    logger.info(f"Retrieving transaction analytics for user ID: {user_id}")
    try:
        analytics = await retrieve_live_transaction_analytics(user_id, start_date, end_date)
        logger.info(f"Transaction analytics retrieved for user ID: {user_id}")
        return ResponseModel(
            analytics,
            "Transaction analytics retrieved successfully",
            status.HTTP_200_OK,
        )
    except EntityDoesNotExistError as e:
        logger.error(f"Transaction analytics not found for user ID: {user_id}")
        raise EntityDoesNotExistError(
            f"Transaction analytics not found for user ID {user_id}"
        )
    except Exception as e:
        logger.error(
            f"An error occurred while retrieving transaction analytics for user ID: {user_id}",
            e,
        )
        raise ServiceError()