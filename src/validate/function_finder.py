import os
from importlib import util
from inspect import getmembers, isfunction
from typing import List, Callable


class ValidateFunctionFinder:
    def __init__(self, path: os.PathLike):
        self.path = path

    def gather_validate_functions(self) -> List[Callable]:
        validation_functions = []
        if self.path:
            spec = util.spec_from_file_location("validation_functions", self.path)
            validate_mod = util.module_from_spec(spec)
            spec.loader.exec_module(validate_mod)
            validation_functions = [
                fx[1]
                for fx in getmembers(validate_mod)
                if fx[0] != "validate" and isfunction(fx[1])
            ]
            from validate import logger
            logger.info(validation_functions)
        return validation_functions
