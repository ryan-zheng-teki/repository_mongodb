import os
import pytest
import time
import logging
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from repository_mongodb.mongo_config import MongoConfig
from repository_mongodb.mongo_client import get_mongo_client, get_mongo_database

# Set up logging
#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def wait_for_mongodb(client, timeout=30):
    """Simple check that MongoDB is ready"""
    logger.debug("Waiting for MongoDB to be ready...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            # Try to ping the server
            client.admin.command('ping')
            logger.debug("Successfully connected to MongoDB")
            return True
        except Exception as e:
            logger.debug(f"Waiting for MongoDB... ({str(e)})")
            time.sleep(1)
    
    return False

@pytest.fixture(scope="session")
def mongo_config():
    logger.debug("Setting up MongoDB configuration")
    os.environ['MONGO_HOST'] = 'localhost'
    os.environ['MONGO_PORT'] = '27017'
    os.environ['MONGO_DATABASE'] = 'test_database'
    os.environ['MONGO_REPLICA_SET'] = 'rs0'
    
    config = MongoConfig()
    logger.debug(f"MongoDB connection URI: {config.get_connection_uri()}")
    return config

@pytest.fixture(scope="session")
def mongo_client(mongo_config):
    logger.debug("Creating MongoDB client")
    client = MongoClient(
        mongo_config.get_connection_uri(),
        serverSelectionTimeoutMS=5000
    )
    
    if not wait_for_mongodb(client):
        pytest.fail("MongoDB not ready within timeout period")
    
    yield client
    client.close()

@pytest.fixture(scope="session")
def mongo_database(mongo_client, mongo_config):
    logger.debug(f"Getting database: {mongo_config.database}")
    return mongo_client[mongo_config.database]

@pytest.fixture(autouse=True)
def cleanup_database(mongo_database):
    yield
    logger.debug("Cleaning up database collections")
    for collection in mongo_database.list_collection_names():
        mongo_database[collection].drop()