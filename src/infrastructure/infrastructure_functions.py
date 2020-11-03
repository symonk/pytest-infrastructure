from typing import Callable, Optional, Set, List, Tuple


class InfrastructureFunction:
    """
    A function wrapper class to store meta data on the collected and executed functions.
    In here lies the 'Infrastructure Function' protocol, encapsulating both meta data and
    execution results to then be subsequently handled by the plugin, driving its behaviour.

    :param real_function: The function object, automatically tracked by the @infrastructure decorator.
    :param order: The order in which the function should be prioritised. 0 being the utmost priority.
    Note: order=-1 will mean the function is disabled, an instance of InfrastructureFunction will never
    be created, as the decorator will filter it out prior to instantiating this wrapper class.
    :param ignored_envs: The environments which the function is not applicable to run against.  This is
    specified via the --infrastructure-envs CLI argument, if absent will assume no function should be ignored.
    :param isolated: By default the execution of infrastructure functions occurs via a thread executor.
    Marking a decorated function as isolated=True will see these functions sequentially executed.

    Some Notes on priority:
     - 0 is the highest priority (0-n there is no upper bound, the premise is on the user to define this).
     - order is only applicable on isolated functions, non isolated will get distributed to the executor
     but there is no guarantee on any completion order there.
     - -1 will have the decorated deemed in a 'disabled' state.
    """

    def __init__(
        self,
        real_function: Callable,
        order: int = 0,
        ignored_envs: Optional[Set[str]] = None,
        isolated: bool = False,
    ):
        self.real_function = real_function
        self.order = order
        self.ignored_envs = ignored_envs or set()
        self.isolated = isolated
        self.result = RunResult()


class RunResult:
    ...


ALL_FUNC_TUPLE_TYPE = Tuple[
    List[Optional[InfrastructureFunction]], List[Optional[InfrastructureFunction]]
]


class InfrastructureFunctionManager:
    """
    List emulation for managing a collection of InfrastructureFunctions
    """

    def __init__(self, infra_functions: List[InfrastructureFunction] = None):
        self.infra_functions = infra_functions or []

    def register(self, infra_func: InfrastructureFunction) -> None:
        """
        In-place sorting of the self.infra_functions automatically when registering a new one.
        """
        self.infra_functions.append(infra_func)
        self.infra_functions.sort(key=lambda x: x.order)

    def get_active(self, env: Optional[str]) -> List[InfrastructureFunction]:
        """
        Fetch the 'active' functions.  By active we mean:
        Functions which are not ignore via the environment; if one is provided.
        """
        return (
            self.infra_functions
            if not env
            else [f for f in self.infra_functions if env not in f.ignored_envs]
        )

    def get_threaded(
        self, env: Optional[str]
    ) -> List[Optional[InfrastructureFunction]]:
        """
        Fetch the active functions which are not marked for isolation.
        """
        return [f for f in self.get_active(env) if not f.isolated]

    def get_isolated(
        self, env: Optional[str]
    ) -> List[Optional[InfrastructureFunction]]:
        """
        Fetch the active functions which are marked for isolation.
        """
        return [f for f in self.get_active(env) if f.isolated]

    def get_applicable(self, env: Optional[str]) -> ALL_FUNC_TUPLE_TYPE:
        """
        Fetch all threaded and isolated functions into a tuple which are applicable to run.
        """
        return self.get_threaded(env), self.get_isolated(env)

    def get_squashed(
        self, env: Optional[str]
    ) -> List[Optional[InfrastructureFunction]]:
        """
        Squash the tuple of threaded vs isolated into one single list.
        """
        return [x for y in self.get_applicable(env) for x in y]

    def __len__(self) -> int:
        return len(self.infra_functions)

    def __getitem__(self, index) -> InfrastructureFunction:
        return self.infra_functions[index]
