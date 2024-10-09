import json
from loguru import logger
from app.config.redis_config import redis_client
from app.config.config import CACHE_EXPIRATION
from app.crud.transactions_service import (
    fetch_transaction_history_from_db,
    fetch_transaction_analytics_from_db,
)


async def refresh_cache(user_id: str):
    try:
        logger.info(f"Refreshing cache for user ID: {user_id}")

        # Refresh transaction history cache
        transaction_history = await fetch_transaction_history_from_db(user_id)
        redis_client.setex(
            f"transaction_history:{user_id}",
            CACHE_EXPIRATION,
            json.dumps(transaction_history),
        )

        # Refresh transaction analytics cache
        transaction_analytics = await fetch_transaction_analytics_from_db(user_id)
        redis_client.setex(
            f"transaction_analytics:{user_id}",
            CACHE_EXPIRATION,
            json.dumps(transaction_analytics),
        )

        logger.info(f"Cache refreshed for user ID: {user_id}")
    except Exception as e:
        logger.error(
            f"An error occurred while refreshing cache for user ID: {user_id}: {e}"
        )
