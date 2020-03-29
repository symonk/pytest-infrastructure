from functools import wraps
from typing import List
from dataclasses import dataclass


@dataclass(repr=True)
class ValidateMeta:
    validate: bool = True
    order: int = 0
    enabled: bool = True
    only_on_env: List = None


def validate(order: int = 0, enabled: bool = True, only_on_env: List = None):
    def real_decorator(func):
        func.meta_data = ValidateMeta(
            order=order, enabled=enabled, only_on_env=only_on_env
        )

        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return real_decorator
