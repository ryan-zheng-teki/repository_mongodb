from functools import wraps
from typing import Any, Callable, Dict, Type, Tuple
import threading

class SingletonMeta(type):
    """
    Thread-safe implementation of the Singleton pattern using metaclass.
    """
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                # Double-checked locking
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class TransactionalMetaclass(type):
    """
    Metaclass that automatically applies transactional decorator to repository methods.
    """
    def __new__(cls, name: str, bases: tuple, attrs: Dict[str, Any]) -> Type:
        transactional_prefixes = (
            "find",
            "create",
            "update",
            "delete",
            "find_by",
            "find_all",
            "find_by_attributes",
        )

        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and any(
                attr_name.startswith(prefix) for prefix in transactional_prefixes
            ):
                attrs[attr_name] = transactional(attr_value)

        return super().__new__(cls, name, bases, attrs)

class RepositoryMetaclass(TransactionalMetaclass):
    """
    Metaclass that handles model type inference for repositories.
    """
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
    Combined metaclass that applies both repository functionality and singleton pattern.
    This ensures that the repository is a singleton and retains repository behaviors.

    This implementation ensures:
    1. Thread-safe singleton pattern
    2. Proper model type inference
    3. Automatic transaction handling
    """
    pass