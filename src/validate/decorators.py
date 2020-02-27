from typing import List


class Validate:
    def __init__(
        self, order: int = 0, enabled: bool = True, run_on_environment: List = None
    ):
        self.order = order
        self.enabled = enabled
        self.run_on_environment = run_on_environment
        self.thread_safe: bool = True

    def __call__(self, func):
        def validate(*args, **kwargs):
            return func(*args, **kwargs)

        return validate
