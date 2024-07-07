import pytest
from repository_mongodb.base_model import BaseModel
from repository_mongodb.mongo_client import get_mongo_database

class TestModel(BaseModel):
    __collection_name__ = "test_collection"

def test_get_collection(mongo_database):
    collection = TestModel.get_collection()
    assert collection.name == "test_collection"
    assert collection.database == get_mongo_database()