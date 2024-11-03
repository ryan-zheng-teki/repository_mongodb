from typing import Tuple, TypeVar, Generic, List, Optional, Type, Any, Dict
from autobyteus.utils.singleton import SingletonMeta

from repository_mongodb.transaction_metaclass import TransactionalMetaclass

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


class SingletonRepositoryMetaclass(RepositoryMetaclass, SingletonMeta):
    """
    Combined metaclass to apply both RepositoryMetaclass and SingletonMeta.
    This ensures that the repository is a singleton and retains repository behaviors.
    """
    pass