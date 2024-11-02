from typing import Tuple, TypeVar, Generic, List, Optional, Type, Any, Dict
from pymongo.collection import Collection

from repository_mongodb.base_model import BaseModel
from repository_mongodb.transaction_metaclass import TransactionalMetaclass

ModelType = TypeVar("ModelType", bound=BaseModel)

class RepositoryMetaclass(TransactionalMetaclass):
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

    def create(self, obj: ModelType, session: Optional[Any] = None) -> ModelType:
        result = self.collection.insert_one(obj.__dict__, session=session)
        obj._id = result.inserted_id
        return obj

    def find_by_id(self, obj_id: str, session: Optional[Any] = None) -> Optional[ModelType]:
        data = self.collection.find_one({"_id": obj_id}, session=session)
        if data:
            return self.model(**data)
        return None

    def find_all(self, session: Optional[Any] = None) -> List[ModelType]:
        return [self.model(**data) for data in self.collection.find(session=session)]

    def find_by_attributes(self, attributes: Dict[str, Any], session: Optional[Any] = None) -> List[ModelType]:
        """
        Find models by specified attributes.
        
        :param attributes: A dictionary of attribute-value pairs to search for.
        :param session: Optional MongoDB session for transaction.
        :return: A list of matching models.
        """
        matching_data = self.collection.find(attributes, session=session)
        matching_data = list(matching_data)
        return [self.model(**data) for data in matching_data]

    def update(self, obj: ModelType, session: Optional[Any] = None) -> ModelType:
        self.collection.replace_one({"_id": obj._id}, obj.__dict__, session=session)
        return obj

    def delete(self, obj: ModelType, session: Optional[Any] = None) -> None:
        self.collection.delete_one({"_id": obj._id}, session=session)