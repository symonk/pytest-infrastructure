from typing import List


class Validate:
    def __init__(
        self,
        order: int = 0,
        enabled: bool = True,
        exclude_on_environment: List = None,
        *args,
        **wa
    ):
        self.order = order
        self.enabled = enabled
        self.exclude_on_environment = exclude_on_environment
        self.thread_safe: bool = True

    def __call__(self, func):
        def validate(*args, **kwargs):
            return func(*args, **kwargs)

        return validate
