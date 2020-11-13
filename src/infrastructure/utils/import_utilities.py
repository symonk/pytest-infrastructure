import importlib.util
from types import ModuleType


def import_module_from_path(module_path: str) -> ModuleType:
    """
    Given a string representing a module path, load the module via the python import machinery.
    """
    spec = importlib.util.spec_from_file_location("infrastructure_functions", module_path)
    infra_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(infra_mod)
    return infra_mod