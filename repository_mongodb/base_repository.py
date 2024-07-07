from typing import TypeVar, Generic, List, Optional, Type, Any, Dict, Tuple
from pymongo.collection import Collection

from repository_mongodb.base_model import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)

class RepositoryMetaclass(type):
    def __new__(cls, name: str, bases: tuple, attrs: Dict[str, Any]) -> Type:
        new_class = super().__new__(cls, name, bases, attrs)
        cls.set_model_attribute(new_class, bases)
        return new_class

    @staticmethod
    def set_model_attribute(new_class: Type, bases: Tuple[Type, ...]) -> None:
        if bases and any(base.__name__ == 'BaseRepository' for base in bases):
            if hasattr(new_class, '__orig_bases__'):
                model_type = new_class.__orig_bases__[0].__args__[0]
                if not hasattr(new_class, 'model') or new_class.model is None:
                    new_class.model = model_type


class BaseRepository(Generic[ModelType], metaclass=RepositoryMetaclass):
    # Subclasses should set this to the concrete model class
    model: ModelType = None
    
    def __init__(self):
        self.collection: Collection = self.model.get_collection()

    def create(self, obj: ModelType) -> ModelType:
        result = self.collection.insert_one(obj.__dict__)
        obj._id = result.inserted_id
        return obj

    def find_by_id(self, obj_id: str) -> Optional[ModelType]:
        data = self.collection.find_one({"_id": obj_id})
        if data:
            return self.model(**data)
        return None

    def find_all(self) -> List[ModelType]:
        return [self.model(**data) for data in self.collection.find()]

    def update(self, obj: ModelType) -> ModelType:
        self.collection.replace_one({"_id": obj._id}, obj.__dict__)
        return obj

    def delete(self, obj: ModelType) -> None:
        self.collection.delete_one({"_id": obj._id})