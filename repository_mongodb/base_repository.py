from typing import Tuple, TypeVar, Generic, List, Optional, Type, Any, Dict
from pymongo.collection import Collection

from repository_mongodb.base_model import BaseModel
from repository_mongodb.metaclasses import SingletonRepositoryMetaclass
from repository_mongodb.mongo_client import session_context_var

ModelType = TypeVar("ModelType", bound=BaseModel)

class BaseRepository(Generic[ModelType], metaclass=SingletonRepositoryMetaclass):
    # Subclasses should set this to the concrete model class
    model: ModelType = None
    
    def __init__(self):
        self.collection: Collection = self.model.get_collection()

    @property
    def session(self):
        return session_context_var.get()

    def create(self, obj: ModelType) -> ModelType:
        result = self.collection.insert_one(obj.__dict__, session=self.session)
        obj._id = result.inserted_id
        return obj

    def find_by_id(self, obj_id: str) -> Optional[ModelType]:
        data = self.collection.find_one({"_id": obj_id}, session=self.session)
        if data:
            return self.model(**data)
        return None

    def find_all(self) -> List[ModelType]:
        return [self.model(**data) for data in self.collection.find(session=self.session)]

    def find_by_attributes(self, attributes: Dict[str, Any]) -> List[ModelType]:
        """
        Find models by specified attributes.
        
        :param attributes: A dictionary of attribute-value pairs to search for.
        :return: A list of matching models.
        """
        matching_data = self.collection.find(attributes, session=self.session)
        matching_data = list(matching_data)
        return [self.model(**data) for data in matching_data]

    def update(self, obj: ModelType) -> ModelType:
        self.collection.replace_one({"_id": obj._id}, obj.__dict__, session=self.session)
        return obj

    def delete(self, obj: ModelType) -> None:
        self.collection.delete_one({"_id": obj._id}, session=self.session)