import os
from inspect import getmembers, isfunction
from typing import List, Callable, Optional
from validate import logger


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
            logger.info([dir(fx) for fx in validate_functions])

        functions = []
        if functions:
            logger.info(f"Found a total of {len(functions)} functions: {functions}")
        return functions
