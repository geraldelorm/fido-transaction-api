import motor.motor_asyncio
from bson.objectid import ObjectId
from app.utils.encryption_utils import encrypt_data, decrypt_data

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.transactions

transaction_collection = database.get_collection("transactions_collection")



def transaction_helper(transaction) -> dict:
    return {
        "id": str(transaction["_id"]),
        "full_name": decrypt_data(transaction["full_name"]),
        "transaction_date": transaction["transaction_date"],
        "transaction_amount": transaction["transaction_amount"],
        "transaction_type": transaction["transaction_type"],
    }

# Retrieve all transactions present in the database
async def retrieve_transactions():
    transactions = []
    async for transaction in transaction_collection.find():
        transactions.append(transaction_helper(transaction))
    return transactions


# Add a new transaction into to the database
async def add_transaction(transaction_data: dict) -> dict:
    transaction = await transaction_collection.insert_one(transaction_data)
    new_transaction = await transaction_collection.find_one({"_id": transaction.inserted_id})
    return transaction_helper(new_transaction)


# Retrieve a transaction with a matching ID
async def retrieve_transaction(id: str) -> dict:
    transaction = await transaction_collection.find_one({"_id": ObjectId(id)})
    if transaction:
        return transaction_helper(transaction)

# Retrieve a transaction with a matching ID
async def retrieve_transaction_history(user_id: str) -> dict:
    transaction = await transaction_collection.find_one({"user_id": str})
    if transaction:
        return transaction_helper(transaction)

# Update a transaction with a matching ID
async def update_transaction(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    transaction = await transaction_collection.find_one({"_id": ObjectId(id)})
    if transaction:
        updated_transaction = await transaction_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_transaction:
            return True
        return False


# Delete a transaction from the database
async def delete_transaction(id: str):
    transaction = await transaction_collection.find_one({"_id": ObjectId(id)})
    if transaction:
        await transaction_collection.delete_one({"_id": ObjectId(id)})
        return True