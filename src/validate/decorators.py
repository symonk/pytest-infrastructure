from functools import wraps
from typing import List


def validate(order: int = 0, enabled: bool = True, exclude_on_environment: List = None):
    @wraps
    def real_decorator(func):
        func.validate = True
        func.order = order
        func.enabled = enabled
        func.exclude_on_environment = exclude_on_environment

        @wraps
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return real_decorator
