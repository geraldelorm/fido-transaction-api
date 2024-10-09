import json
from bson.objectid import ObjectId
from app.models.transaction_model import TransactionModel
from app.utils.encryption_utils import decrypt_data
from app.database.database import transaction_collection
from loguru import logger
from app.config.redis_config import redis_client
from app.config.config import CACHE_EXPIRATION

from app.exceptions.exceptions import FidoTransactionAPIError, EntityDoesNotExistError


async def add_transaction(transaction_data: dict) -> dict:
    try:
        new_transaction = await transaction_collection.insert_one(transaction_data)
        logger.info("New record added")
        created_transaction = await transaction_collection.find_one(
            {"_id": new_transaction.inserted_id}
        )
        logger.info("Added a transaction record")
        return transaction_helper(created_transaction)
    except Exception as e:
        logger.error("An error occurred while adding a transaction record", e)
        raise FidoTransactionAPIError(
            "An error occurred while adding a transaction record"
        )


async def retrieve_transaction(id: str) -> dict:
    transaction_id = validate_id(id)
    transaction = await transaction_collection.find_one({"_id": transaction_id})
    if transaction:
        logger.info(f"Transaction found for ID: {id}")
        try:
            return transaction_helper(transaction)
        except Exception as e:
            logger.error(
                f"An error occurred while transforming fields in transaction data for ID: {id}",
                e,
            )
            logger.error(f"Error data: {e}")
            raise FidoTransactionAPIError(
                "An error occurred while transforming fields in transaction data"
            )
    else:
        raise EntityDoesNotExistError("Transaction not found.")


async def retrieve_transaction_history(user_id: str) -> dict:
    cache_key = f"transaction_history:{user_id}"
    cached_data = redis_client.get(cache_key)

    if cached_data:
        logger.info(f"Cache hit for transaction history of user ID: {user_id}")
        return json.loads(cached_data)

    logger.info(f"Cache miss for transaction history of user ID: {user_id}")

    transactions = await transaction_collection.find({"user_id": user_id}).to_list(
        length=100
    )
    res = []
    if len(transactions) > 0:
        for transaction in transactions:
            res.append(transaction_helper(transaction))

        redis_client.setex(cache_key, CACHE_EXPIRATION, json.dumps(res))

        return res
    else:
        raise EntityDoesNotExistError("No transactions found for the given user ID.")


async def update_transaction(id: str, data: dict):
    transaction_id = validate_id(id)
    if len(data) < 1:
        return False
    transaction = await transaction_collection.find_one({"_id": transaction_id})
    if transaction:
        updated_transaction = await transaction_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_transaction:
            # Invalidate the cache for the user
            user_id = transaction["user_id"]
            cache_key = f"transaction_history:{user_id}"
            redis_client.delete(cache_key)
            logger.info(f"Cache invalidated for user ID: {user_id}")
            return True
        return False
    else:
        raise EntityDoesNotExistError("No transactions found for the given user ID.")


async def delete_transaction(id: str):
    transaction_id = validate_id(id)
    transaction = await transaction_collection.find_one({"_id": transaction_id})
    if transaction:
        await transaction_collection.delete_one({"_id": ObjectId(id)})
        return True
    else:
        raise EntityDoesNotExistError(
            f"No transactions found for the given user ID: {id}"
        )


def validate_id(id: str) -> ObjectId:
    try:
        transaction_id = ObjectId(id)
        return transaction_id
    except Exception:
        raise EntityDoesNotExistError(f"Transaction id: {id} is Not Found")


def transaction_helper(transaction: TransactionModel) -> dict:
    return {
        "id": str(transaction["_id"]),
        # "full_name": decrypt_data(transaction["full_name"]),
        "transaction_date": transaction["transaction_date"],
        "transaction_amount": transaction["transaction_amount"],
        "transaction_type": transaction["transaction_type"],
    }
