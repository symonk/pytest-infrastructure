from typing import Callable, Optional, Set


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
