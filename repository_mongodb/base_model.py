from typing import Optional
from bson import ObjectId

from repository_mongodb.mongo_client import get_mongo_database

class BaseModel:
    __collection_name__: str
    _id: Optional[ObjectId]

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def get_collection(cls):
        return get_mongo_database()[cls.__collection_name__]