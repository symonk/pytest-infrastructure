# -*- coding: utf-8 -*-
import functools
from concurrent.futures._base import Future
from typing import List, Set, Optional

import pytest
from _pytest.config import PytestPluginManager, Config

from infrastructure import InfrastructureFunction
from infrastructure import InfrastructureFunctionManager
from infrastructure.utils.plugin_utilities import can_plugin_be_registered
from infrastructure.utils.constants import INFRASTRUCTURE_PLUGIN_NAME
import logging

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
    from infrastructure.hooks.hookspecs import InfrastructureHookSpecs

    pluginmanager.add_hookspecs(InfrastructureHookSpecs)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if can_plugin_be_registered(config):
        infra_plugin = PytestValidate(config)
        config.pluginmanager.register(infra_plugin, INFRASTRUCTURE_PLUGIN_NAME)
        config.pluginmanager.hook.pytest_infrastructure_collect_modifyitems(items=[])
        infra_plugin.validate_infrastructure(config)


class PytestValidate:
    """
    The pytest infrastructure plugin object;
    This plugin is only registered if the --bypass-infrastructure arg is not provided, else it is completely skipped!
    """

    _infrastructure_manager: InfrastructureFunctionManager = InfrastructureFunctionManager()

    def __init__(self, config):
        self.config = config
        self.functions = None
        self.environment = config.getoption("infra_env")
        self.thread_count = config.getoption("parallel_bounds")

    @pytest.hookimpl(tryfirst=True)
    def pytest_infrastructure_collect_modifyitems(
        self, items: List[InfrastructureFunction]
    ) -> None:
        """
        Default behaviour is to use the infrastructure functions which have been imported.
        """
        items[:] = self._infrastructure_manager.get_applicable(self.environment)

    @classmethod
    def register(cls, wrapper_func: InfrastructureFunction) -> None:
        cls._infrastructure_manager.register(wrapper_func)

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

        parallel, isolated = self._infrastructure_manager.get_applicable(
            self.environment
        )
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
        return self._infrastructure_manager.get_squashed(self.environment)

    @pytest.hookimpl()
    def pytest_report_header(self, config: Config) -> str:
        if config.getoption("verbose") > 0:
            message = (
                "".join(
                    [
                        fx.__name__
                        for fx in self._infrastructure_manager.get_squashed(
                            self.environment
                        )
                    ]
                )
                or "In Infrastructure functions."
            )
            return message


def infrastructure(ignored_on: Optional[Set[str]] = None, order: int = -1):
    """
    Bread and button of pytest-infrastructure.  Stores implementations of the decorator globally
    which are then available to the PytestValidate plugin to invoke and apply its custom logic to the pytest run.
    """

    def decorator(func):
        wrapper = InfrastructureFunction(
            executable=func, ignored_on=ignored_on, order=order
        )
        PytestValidate.register(wrapper)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator
