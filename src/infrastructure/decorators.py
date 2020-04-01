from functools import wraps
from typing import List
from dataclasses import dataclass


@dataclass(repr=True)
class InfrastructureMeta:
    validate: bool = True
    order: int = 0
    enabled: bool = True
    only_on_env: str = None
    isolated: bool = False
    name: str = None


def infrastructure(
    order: int = 0,
    enabled: bool = True,
    only_on_env: str = None,
    isolated: bool = False,
):
    def real_decorator(func):
        func.meta_data = InfrastructureMeta(
            order=order,
            enabled=enabled,
            only_on_env=only_on_env,
            isolated=isolated,
            name=func.__name__,
        )

        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return real_decorator
