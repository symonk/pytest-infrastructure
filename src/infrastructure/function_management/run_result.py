from typing import Any
from typing import Optional


class Result:
    def __init__(self, name: str, status: str, uuid: str):
        self.name = name
        self.status = status
        self.uuid = uuid
        self.exec_result: Optional[Any] = None

    def __repr__(self) -> str:
        return str(vars(self))
