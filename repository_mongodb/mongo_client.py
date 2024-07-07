from pymongo import MongoClient
from repository_mongodb.mongo_config import MongoConfig

_mongo_client = None
_mongo_database = None

def get_mongo_client():
    global _mongo_client
    if _mongo_client is None:
        mongo_config = MongoConfig()
        _mongo_client = MongoClient(mongo_config.get_connection_uri())
    return _mongo_client

def get_mongo_database():
    global _mongo_database
    if _mongo_database is None:
        mongo_config = MongoConfig()
        _mongo_database = get_mongo_client()[mongo_config.database]
    return _mongo_database