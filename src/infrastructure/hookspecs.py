from collections import Callable
from typing import List

from pluggy import HookspecMarker, HookimplMarker


hookspec = HookspecMarker("pytest")
hookimpl = HookimplMarker("pytest")


class InfrastructureHookSpecs:
    @hookspec()
    def pytest_infrastructure_collect_modifyitems(self, items: List[Callable]) -> None:
        """ Hook for performing the collection of infrastructure functions.
            items should be modified in place. similar to pytest collection modifyitems.
        """
        ...