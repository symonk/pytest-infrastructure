from collections.abc import Callable
from typing import Optional
from typing import Set

from .run_result import RunResult


class InfrastructureFunction:
    def __init__(
        self,
        executable: Callable,
        ignored_on: Optional[Set[str]] = None,
        order: int = 0,
        name: Optional[str] = None,
    ):
        self.executable = executable
        self.ignored_on = ignored_on or set()
        self.order = order
        self.name = (
            executable.__name__ if name is None or not name.strip() else name.strip()
        )
        self.result = RunResult()

    def _resolve_status(self) -> str:
        statuses = {-1: "<Disabled>", 0: "<Concurrent>"}
        return statuses.get(self.order, "<Sequential>")

    def __call__(self, *args, **kwargs) -> RunResult:
        return self.executable(*args, **kwargs)

    def __repr__(self) -> str:
        return f"{self.name}: {repr(self.result)} | Status: {self._resolve_status()}"
