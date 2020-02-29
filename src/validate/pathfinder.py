import os
from typing import List, Callable, Optional


class ValidateFunctionFinder:
    def __init__(self, path: Optional[os.PathLike]):
        self.path = path

    def gather_validate_functions(self) -> List[Callable]:
        functions = []
        print(self.path)
        print(f"Found the following validate functions: {functions}")
        return functions

    def _runpy_load_module(self):
        pass

    def _collect_functions_from_module(self):
        pass
