from __future__ import annotations
from typing import Optional, List, Tuple
from . import InfrastructureFunction

ALL_FUNC_TUPLE_TYPE = Tuple[
    List[Optional[InfrastructureFunction]], List[Optional[InfrastructureFunction]]
]


class InfrastructureFunctionManager:
    """
    List emulation for managing a collection of InfrastructureFunctions
    """

    def __init__(self, infra_functions: List[InfrastructureFunction] = None):
        self.infra_functions = infra_functions or []
        self._sort()

    def register(
        self, infra_func: InfrastructureFunction
    ) -> InfrastructureFunctionManager:
        """
        In-place sorting of the self.infra_functions automatically when registering a new one.
        returns the manager instance for fluency.
        """
        self.infra_functions.append(infra_func)
        self._sort()
        return self

    def _sort(self) -> None:
        self.infra_functions.sort(key=lambda x: x.order)

    def get_active(self, env: Optional[str] = None) -> List[InfrastructureFunction]:
        """
        Fetch the 'active' functions.  By active we mean:
        Functions which are not ignore via the environment; if one is provided.
        """

        if env:
            funcs = [f for f in self.infra_functions if env not in f.ignored_on]
            return funcs
        return self.infra_functions

    def get_threaded(
        self, env: Optional[str] = None
    ) -> List[Optional[InfrastructureFunction]]:
        """
        Fetch the active functions which are not marked for isolation.
        """
        return [f for f in self.get_active(env) if f.order != -1]

    def get_isolated(
        self, env: Optional[str] = None
    ) -> List[Optional[InfrastructureFunction]]:
        """
        Fetch the active functions which are marked for isolation.
        """
        return [f for f in self.get_active(env) if f.order == -1]

    def get_applicable(self, env: Optional[str] = None) -> ALL_FUNC_TUPLE_TYPE:
        """
        Fetch all threaded and isolated functions into a tuple which are applicable to run.
        """
        return self.get_threaded(env), self.get_isolated(env)

    def get_squashed(
        self, env: Optional[str] = None
    ) -> List[Optional[InfrastructureFunction]]:
        """
        Squash the tuple of threaded vs isolated into one single list.
        """
        return [x for y in self.get_applicable(env) for x in y]

    def __len__(self) -> int:
        return len(self.infra_functions)

    def __getitem__(self, index) -> InfrastructureFunction:
        return self.infra_functions[index]
