import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from repository_mongodb.mongo_config import MongoConfig

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

_mongo_client = None
_mongo_database = None

def get_mongo_client():
    global _mongo_client
    if _mongo_client is None:
        mongo_config = MongoConfig()
        connection_uri = mongo_config.get_connection_uri()
        logger.debug(f"Connecting to MongoDB with URI: {connection_uri}")
        
        try:
            _mongo_client = MongoClient(
                connection_uri,
                serverSelectionTimeoutMS=5000
            )
            # Test connection
            _mongo_client.admin.command('ping')
            logger.debug("Successfully connected to MongoDB")
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise
        except ServerSelectionTimeoutError as e:
            logger.error(f"Server selection timeout: {str(e)}")
            raise
            
    return _mongo_client

def get_mongo_database():
    global _mongo_database
    if _mongo_database is None:
        mongo_config = MongoConfig()
        client = get_mongo_client()
        _mongo_database = client[mongo_config.database]
        logger.debug(f"Connected to database: {mongo_config.database}")
    return _mongo_database