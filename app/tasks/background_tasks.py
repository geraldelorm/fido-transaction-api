from loguru import logger


async def update_user_statistics(user_id: str):
    try:
        logger.info(f"User statistics updated for user ID: {user_id}")
    except Exception as e:
        logger.error(
            f"An error occurred while updating user statistics for user ID: {user_id}: {e}"
        )


async def alert_relevant_systems(transaction):
    try:
        logger.info(f"Alert sent for transaction ID: {transaction}")
    except Exception as e:
        logger.error(
            f"An error occurred while sending alert for transaction ID: {transaction.transaction_id}: {e}"
        )


async def recalculate_credit_scores(user_id: str):
    try:
        logger.info(f"Credit score recalculated for user ID: {user_id}")
    except Exception as e:
        logger.error(
            f"An error occurred while recalculating credit score for user ID: {user_id}: {e}"
        )
