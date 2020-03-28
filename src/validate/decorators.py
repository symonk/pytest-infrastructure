from functools import wraps
from typing import List


def validate(order: int = 0, enabled: bool = True, only_on_env: List = None):
    @wraps
    def real_decorator(func):
        func.validate = True
        func.order = order
        func.enabled = enabled
        func.only_on_env = only_on_env

        @wraps
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return real_decorator
