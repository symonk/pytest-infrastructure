import uuid
from collections.abc import Callable
from typing import Optional
from typing import Set

from .run_result import Result


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
        self.uuid = str(uuid.uuid4())
        self.result = Result(self.name, self._resolve_status(), self.uuid)

    def _resolve_status(self) -> str:
        statuses = {-1: "<Disabled>", 0: "<Concurrent>"}
        return statuses.get(self.order, "<Sequential>")

    def __call__(self, *args, **kwargs) -> Result:
        """
        Calls the wrapped function.
        """
        try:
            result = self.executable(*args, **kwargs)
            self.result.exec_result = (True, "Passed!")
            return result
        except Exception as exc:
            self.result.exec_result = (False, "Failed!", exc)

    def __repr__(self) -> str:
        return repr(self.result)
