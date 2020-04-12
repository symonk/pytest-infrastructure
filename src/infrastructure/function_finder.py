from importlib import util
from inspect import getmembers
from typing import List, Callable


class FunctionFinder:
    def __init__(self, path: str):
        self.path = path

    def gather_infrastructure_functions(self) -> List[Callable]:
        validation_functions = []
        if self.path:
            spec = util.spec_from_file_location("validation_functions", self.path)
            validate_mod = util.module_from_spec(spec)
            spec.loader.exec_module(validate_mod)
            validation_functions = [
                fx[1] for fx in getmembers(validate_mod) if hasattr(fx[1], "meta_data")
            ]
        return validation_functions
