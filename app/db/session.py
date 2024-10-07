# # app/db/session.py

# from app.core.config import settings
# from app.__version__ import __version__
# from motor import motor_asyncio, core
# from pymongo.driver_info import DriverInfo

# # Define the driver info with application version
# DRIVER_INFO = DriverInfo(name="fido-transactions- fastapi-mongodb", version=__version__)

# class _MongoClientSingleton:
#     mongo_client: motor_asyncio.AsyncIOMotorClient | None
#     engine: motor_asyncio.AsyncIOMotorClient | None

#     def __new__(cls):
#         if not hasattr(cls, "instance"):
#             cls.instance = super(_MongoClientSingleton, cls).__new__(cls)
#             # Initialize the MongoDB client
#             cls.instance.mongo_client = motor_asyncio.AsyncIOMotorClient(
#                 settings.MONGO_DATABASE_URI, driver=DRIVER_INFO
#             )
#         return cls.instance

# def MongoDatabase() -> core.AgnosticDatabase:
#     return _MongoClientSingleton().mongo_client[settings.MONGO_DATABASE]

# async def ping():
#     await MongoDatabase().command("ping")

# __all__ = ["MongoDatabase", "ping"]
