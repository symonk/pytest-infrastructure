from collections import Callable
from typing import Optional, Set
from .run_result import RunResult


class InfrastructureFunction:
    def __init__(
        self,
        executable: Callable,
        ignored_on: Optional[Set[str]] = None,
        order: int = -1,
    ):
        self.executable = executable
        self.ignored_on = ignored_on or set()
        self.order = order
        self.result = RunResult()

    def __call__(self, *args, **kwargs) -> RunResult:
        return self.executable(*args, **kwargs)
