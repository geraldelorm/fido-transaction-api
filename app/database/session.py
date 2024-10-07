from motor.motor_asyncio import AsyncIOMotorClient
from app.exceptions.exceptions import ServiceError

class DBSessionManager:
        def __init__(self, uri: str, database_name: str):
            self.client = AsyncIOMotorClient(uri)
            self.db = self.client[database_name]