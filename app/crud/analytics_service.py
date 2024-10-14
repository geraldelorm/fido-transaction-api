import json
from datetime import datetime

from loguru import logger

from app.config.config import CACHE_EXPIRATION
from app.config.redis_config import redis_client
from app.database.database import analytics_collection, transaction_collection
from app.exceptions.exceptions import EntityDoesNotExistError, ServiceError
from app.models.analytics_model import AnalyticsModel


async def compute_and_store_analytics():
    logger.info("Computing and storing analytics data")
    try:
        users = await transaction_collection.distinct("user_id")
        for user_id in users:
            query = {"user_id": user_id}

            logger.info(f"Analytics query: `{query}`")

            transactions = await transaction_collection.find(query).to_list(length=None)

            logger.info(
                f"Transactions retrieved for user ID: {user_id} - processing analytics next"
            )

            if not transactions:
                continue

            total_value = sum(t["transaction_amount"] for t in transactions)
            average_value = total_value / len(transactions)

            logger.info(f"Total value: {total_value}, Average value: {average_value}")

            transactions_by_day = {}
            for t in transactions:
                day = t["transaction_date"]
                if day not in transactions_by_day:
                    transactions_by_day[day] = 0
                transactions_by_day[day] += 1

            logger.info(f"Transactions by day: {transactions_by_day}")

            highest_transactions_day = max(
                transactions_by_day, key=transactions_by_day.get
            )

            debit_total = sum(
                t["transaction_amount"]
                for t in transactions
                if t["transaction_type"] == "debit"
            )
            credit_total = sum(
                t["transaction_amount"]
                for t in transactions
                if t["transaction_type"] == "credit"
            )

            logger.info(f"Debit total: {debit_total}, Credit total: {credit_total}")

            analytics_data = {
                "user_id": user_id,
                "average_transaction_value": average_value,
                "highest_transactions_day": highest_transactions_day,
                "debit_total": debit_total,
                "credit_total": credit_total,
                "last_updated": datetime.now(),
            }

            logger.info(f"Analytics data computed for user ID: {user_id}")

            await analytics_collection.update_one(
                {"user_id": user_id}, {"$set": analytics_data}, upsert=True
            )
            logger.info(f"Analytics data updated for user ID: {user_id}")

    except Exception as e:
        logger.error("An error occurred while computing and storing analytics data", e)
        raise ServiceError()


async def retrieve_transaction_analytics(user_id: str) -> AnalyticsModel:
    cache_key = f"transaction_analytics:{user_id}"
    cached_data = redis_client.get(cache_key)

    if cached_data:
        logger.info(f"Cache hit for transaction analytics of user ID: {user_id}")
        return json.loads(cached_data)

    logger.info(f"Cache miss for transaction analytics of user ID: {user_id}")

    analytics = await analytics_collection.find_one({"user_id": user_id})
    if not analytics:
        try:
            analytics = await retrieve_live_transaction_analytics(user_id)
        except EntityDoesNotExistError as e:
            logger.error(f"Transaction analytics not found for user ID: {user_id}")
            raise EntityDoesNotExistError(
                f"Transaction analytics not found for user ID {user_id}"
            )

    analytics["_id"] = str(analytics["_id"])
    analytics["last_updated"] = analytics["last_updated"].isoformat()
    redis_client.setex(cache_key, CACHE_EXPIRATION, json.dumps(analytics))

    return AnalyticsModel(**analytics)

# For when scheduled task yields no result
async def retrieve_live_transaction_analytics(
    user_id: str, start_date: datetime = None, end_date: datetime = None
):
    query = {"user_id": user_id}
    if start_date and end_date:
        query["transaction_date"] = {
            "$gte": start_date.isoformat(timespec="microseconds"),
            "$lte": end_date.isoformat(timespec="microseconds"),
        }

    logger.info(f"Analytics query: `{query}`")

    transactions = await transaction_collection.find(query).to_list(length=None)

    logger.info(
        f"Transactions retrieved for user ID: {user_id} - processing analytics next"
    )

    if not transactions:
        raise EntityDoesNotExistError(
            f"Transaction analytics not found for user ID {user_id} - Please check time range e.g 2024-10-08T01:05:37.574299"
        )

    total_value = sum(t["transaction_amount"] for t in transactions)
    average_value = total_value / len(transactions)

    logger.info(f"Total value: {total_value}, Average value: {average_value}")

    transactions_by_day = {}
    for t in transactions:
        day = t["transaction_date"]
        if day not in transactions_by_day:
            transactions_by_day[day] = 0
        transactions_by_day[day] += 1

    logger.info(f"Transactions by day: {transactions_by_day}")

    highest_transactions_day = max(transactions_by_day, key=transactions_by_day.get)

    debit_total = sum(
        t["transaction_amount"]
        for t in transactions
        if t["transaction_type"] == "debit"
    )
    credit_total = sum(
        t["transaction_amount"]
        for t in transactions
        if t["transaction_type"] == "credit"
    )

    logger.info(f"Debit total: {debit_total}, Credit total: {credit_total}")

    return {
        "average_transaction_value": average_value,
        "highest_transactions_day": highest_transactions_day,
        "debit_total": debit_total,
        "credit_total": credit_total,
    }
