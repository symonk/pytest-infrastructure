from collections.abc import Callable
from typing import Optional
from typing import Set

from .run_result import RunResult


class InfrastructureFunction:
    def __init__(
        self,
        executable: Callable,
        ignored_on: Optional[Set[str]] = None,
        order: int = -1,
        name: Optional[str] = None,
    ):
        self.executable = executable
        self.ignored_on = ignored_on or set()
        self.order = order
        self.name = name if name.strip() else executable.__name__
        self.result = RunResult()

    def __call__(self, *args, **kwargs) -> RunResult:
        return self.executable(*args, **kwargs)

    def __repr__(self) -> str:
        return f"{self.name}: {repr(self.result)}"
