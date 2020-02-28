import os
from typing import List, Callable, Optional


class ValidateFunctionFinder:
    def __init__(self, path: Optional[os.PathLike]):
        self.path = path

    def gather_validate_functions(self) -> List[Callable]:
        functions = []
        return functions
