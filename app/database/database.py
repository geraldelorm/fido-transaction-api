from motor.motor_asyncio import AsyncIOMotorClient

from app.config.config import (FIDO_ANALYTICS_COLLECTION,
                               FIDO_TRANSACTIONS_COLLECTION, MONGO_DB_NAME,
                               MONGODB_URI)


class DBSessionManager:
    def __init__(self, uri: str, database_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[database_name]


class MongoDBSessionManager(DBSessionManager):

    def get_collection(self, collection_name: str):
        return self.db.get_collection(collection_name)


mongodb_session_manager = MongoDBSessionManager(
    uri=MONGODB_URI, database_name=MONGO_DB_NAME
)

transaction_collection = mongodb_session_manager.get_collection(
    FIDO_TRANSACTIONS_COLLECTION
)

analytics_collection = mongodb_session_manager.get_collection(FIDO_ANALYTICS_COLLECTION)
