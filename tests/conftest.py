import os
import pytest
from pymongo import MongoClient
from repository_mongodb.mongo_config import MongoConfig
from repository_mongodb.mongo_client import get_mongo_client, get_mongo_database

@pytest.fixture(scope="session")
def mongo_config():
    return MongoConfig()

@pytest.fixture(scope="session")
def mongo_client(mongo_config):
    client = MongoClient(mongo_config.get_connection_uri())
    yield client
    client.close()

@pytest.fixture(scope="session")
def mongo_database(mongo_client, mongo_config):
    return mongo_client[mongo_config.database]

@pytest.fixture(autouse=True)
def setup_mongo_env(monkeypatch):
    monkeypatch.setenv('MONGO_HOST', 'localhost')
    monkeypatch.setenv('MONGO_PORT', '27017')
    monkeypatch.setenv('MONGO_USERNAME', '')
    monkeypatch.setenv('MONGO_PASSWORD', '')
    monkeypatch.setenv('MONGO_DATABASE', 'test_database')

@pytest.fixture(scope="function", autouse=True)
def clean_mongo_data(mongo_database):
    yield
    
    collection = mongo_database["test_collection"]
    collection.drop()