from typing import List
from functools import wraps


def validate(order: int = 0, enabled: bool = True, exclude_on_environment: List = None):
    @wraps
    def real_decorator(func):
        func.validate = True
        func.order = order
        func.enabled = enabled
        func.exclude_on_environment = exclude_on_environment

        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return real_decorator
