from functools import wraps
from typing import Any, Callable, Dict, Type, Tuple

from repository_mongodb.transaction_management import transactional

class TransactionalMetaclass(type):
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