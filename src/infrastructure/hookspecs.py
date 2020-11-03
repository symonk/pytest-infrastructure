from collections import Callable
from typing import List

from pluggy import HookspecMarker, HookimplMarker


hookspec = HookspecMarker("pytest")
hookimpl = HookimplMarker("pytest")


class InfrastructureHookSpecs:
    @hookspec(firstresult=True)
    def pytest_infrastructure_collect(self) -> List[Callable]:
        """ Hook for performing the collection of infrastructure functions.
            Implement your own hook and return the List[Callable] functions which adhere to what you desire. """

    @hookspec()
    def pytest_infrastructure_validate(self, functions: List[Callable]):
        """ Hook for performing the execution of infrastructure functions """
