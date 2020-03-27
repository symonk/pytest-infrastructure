import os
from inspect import getmembers, isfunction
from typing import List, Callable, Optional


class ValidateFunctionFinder:
    def __init__(self, path: Optional[os.PathLike]):
        self.path = path

    def gather_validate_functions(self) -> List[Callable]:
        if self.path:
            from importlib import util

            spec = util.spec_from_file_location("validation_functions", self.path)
            validate_mod = util.module_from_spec(spec)
            spec.loader.exec_module(validate_mod)
            validate_functions = [
                fx for fx in getmembers(validate_mod) if isfunction(fx[1])
            ]
            print([dir(fx) for fx in validate_functions])

        functions = []
        if functions:
            print(f"Found a total of {len(functions)} functions: {functions}")
        return functions

    def gather_validate_functions_2(self):
        pass

    def _runpy_load_module(self):
        pass

    def _collect_functions_from_module(self):
        pass
