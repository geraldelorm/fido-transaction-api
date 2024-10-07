from app.config.config import MONGO_URI, MONGO_DB_NAME, FIDO_TRANSACTIONS_COLLECTION
from app.database.session import DBSessionManager

class MongoDBSessionManager(DBSessionManager):

      def get_collection(self, collection_name: str):
            return self.db.get_collection(collection_name)

mongodb_session_manager = MongoDBSessionManager(uri=MONGO_URI, database_name=MONGO_DB_NAME)

transaction_collection = mongodb_session_manager.get_collection(FIDO_TRANSACTIONS_COLLECTION)