# -*- coding: utf-8 -*-
import functools
import logging
from concurrent.futures._base import Future
from typing import List
from typing import Optional
from typing import Set

import pytest
from _pytest.config import Config
from _pytest.config import PytestPluginManager
from _pytest.terminal import TerminalReporter
from infrastructure import InfrastructureFunction
from infrastructure import InfrastructureFunctionManager
from infrastructure.utility.constants import INFRASTRUCTURE_PLUGIN_NAME
from infrastructure.utility.import_utilities import import_module_from_path
from infrastructure.utility.plugin_utilities import can_plugin_be_registered

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    group = parser.getgroup(INFRASTRUCTURE_PLUGIN_NAME)
    group.addoption(
        "--skip-infra",
        action="store_true",
        default=False,
        dest="skip_infra",
        help="Bypass the validation functions and execute testing without checking, disable the plugin completely",
    )
    group.addoption(
        "--infra-module",
        action="store",
        dest="infra_module",
        help="Module containing @infrastructure decorated functions",
    )
    group.addoption(
        "--parallel-bounds",
        action="store",
        type=int,
        default=2,
        dest="parallel_bounds",
        help="If specified will use threads to execute infrastructure threads in parallel",
    )
    group.addoption(
        "--infra-env",
        action="store",
        type=list,
        dest="infra_env",
        help="Runtime environment; only_on_env= of validation functions will account for this"
        "Note: if not specified, all infrastructure functions will be executed.",
    )
    group.addoption(
        "--use-processes",
        action="store_true",
        default=False,
        dest="use_processes",
        help="Execute via a process pool, rather than a thread pool."
        "Depending on IO bound etc, your infra functions may be better "
        "distributed via processes, not threads.",
    )


@pytest.hookimpl
def pytest_addhooks(pluginmanager: PytestPluginManager) -> None:
    from infrastructure.hookspecs import InfrastructureHookSpecs

    pluginmanager.add_hookspecs(InfrastructureHookSpecs)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if can_plugin_be_registered(config):
        infra_plugin = PytestValidate(config)
        config.pluginmanager.register(infra_plugin, INFRASTRUCTURE_PLUGIN_NAME)
        collected = config.pluginmanager.hook.pytest_infrastructure_perform_collect(
            module_path=config.getoption("infra_module")
        )
        config.pluginmanager.hook.pytest_infrastructure_collect_modifyitems(
            items=collected[0]
        )
        infra_plugin.validate_infrastructure(config)


class PytestValidate:
    """
    The pytest infrastructure plugin object;
    This plugin is only registered if the --bypass-infrastructure arg is not provided, else it is completely skipped!
    """

    def __init__(self, config):
        self.config = config
        self.functions = None
        self.environment = config.getoption("infra_env")
        self.thread_count = config.getoption("parallel_bounds")
        self.infra_module = config.getoption("infra_module")
        self.infra_manager: InfrastructureFunctionManager = InfrastructureFunctionManager()

    @pytest.hookimpl(tryfirst=True)
    def pytest_infrastructure_perform_collect(
        self, module_path: str
    ) -> List[InfrastructureFunction]:
        infra_mod = import_module_from_path(module_path)
        from inspect import isfunction, getmembers

        infra_functions = [
            InfrastructureFunction(
                executable=func[1],
                name=func[1].name,
                order=func[1].order,
                ignored_on=func[1].ignored_on,
            )
            for func in getmembers(infra_mod)
            if isfunction(func[1]) and hasattr(func[1], "is_infra")
        ]
        return infra_functions

    @pytest.hookimpl(tryfirst=True)
    def pytest_infrastructure_collect_modifyitems(
        self, items: List[Optional[InfrastructureFunction]]
    ) -> None:
        """
        Default behaviour is to use the infrastructure functions which have been imported.
        """
        for func in items:
            self.infra_manager.register(func)
        items[:] = self.infra_manager.get_applicable(self.environment)

    def validate_infrastructure(self, config: Config) -> None:
        from concurrent.futures import ThreadPoolExecutor
        from concurrent.futures import ProcessPoolExecutor
        from concurrent.futures import as_completed

        bound_count = config.getoption("parallel_bounds")
        executor_instance = (
            ThreadPoolExecutor
            if not config.getoption("use_processes")
            else ProcessPoolExecutor
        )

        parallel, isolated = self.infra_manager.get_applicable(self.environment)
        run_results = []
        with executor_instance(max_workers=bound_count) as executor:
            futures: List[Future] = []
            for non_isolated_function in parallel:
                futures.append(executor.submit(non_isolated_function.executable))
            for future in as_completed(futures):
                try:
                    run_results.append(future.result())
                except Exception as exc:
                    # These are user defined, we need to catch anything here.
                    run_results.append(exc)

    @pytest.fixture
    def infra_functions(self) -> List[InfrastructureFunction]:
        return self.infra_manager.get_squashed(self.environment)

    @pytest.hookimpl()
    def pytest_terminal_summary(self, terminalreporter: TerminalReporter) -> None:
        functions = self.infra_manager.get_squashed(self.environment)
        terminalreporter.write_sep("-", "pytest-infrastructure results")
        if not functions:
            terminalreporter.write_line(
                "no pytest-infrastructure functions collected & executed."
            )
        else:
            for function in functions:
                terminalreporter.write_line(repr(function))


def infrastructure(
    ignored_on: Optional[Set[str]] = None, order: int = -1, name: str = None
):
    """
    Bread and button of pytest-infrastructure.  Stores implementations of the decorator globally
    which are then available to the PytestValidate plugin to invoke and apply its custom logic to the pytest run.
    """

    def decorator(func):
        func.ignored_on = ignored_on
        func.order = order
        func.is_infra = True
        func.name = name or func.__name__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator
