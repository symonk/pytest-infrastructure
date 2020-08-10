from functools import wraps
from typing import List
from dataclasses import dataclass, field

INFRASTRUCTURE_FUNCTIONS = []


@dataclass(repr=True)
class InfrastructureMeta:
    validate: bool = True
    order: int = 0
    enabled: bool = True
    not_on_env: List = field(default_factory=lambda: [])
    isolated: bool = False
    name: str = None


def infrastructure(
    order: int = 0,
    enabled: bool = True,
    not_on_env: List = None,
    isolated: bool = False,
):
    def real_decorator(func):
        func.meta_data = InfrastructureMeta(
            order=order,
            enabled=enabled,
            not_on_env=not_on_env or [],
            isolated=isolated,
            name=func.__name__,
        )
        INFRASTRUCTURE_FUNCTIONS.append(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return real_decorator
