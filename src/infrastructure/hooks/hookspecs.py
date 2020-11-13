from collections import Callable
from typing import List

from pluggy import HookimplMarker
from pluggy import HookspecMarker


hookspec = HookspecMarker("pytest")
hookimpl = HookimplMarker("pytest")


class InfrastructureHookSpecs:

    @hookspec()
    def pytest_infrastructure_perform_collect(self, module_path: str) -> List[Callable]:
        """ Hook for performing the collection of infra structure functions, given the
            path to the module which contains them via the command line interface.
        """
        ...

    @hookspec()
    def pytest_infrastructure_collect_modifyitems(self, items: List[Callable]) -> None:
        """ Hook for performing the collection of infrastructure functions.
            items should be modified in place. similar to pytest collection modifyitems.
        """
        ...
