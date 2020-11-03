# -*- coding: utf-8 -*-
import functools
from typing import List, Set, Optional

import pytest
from _pytest.config import PytestPluginManager, Config

from infrastructure.infrastructure_functions import (
    InfrastructureFunction,
    InfrastructureFunctionManager,
)
from infrastructure.plugin_utilities import can_plugin_be_registered
from infrastructure.strings import INFRASTRUCTURE_PLUGIN_NAME
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
        "--infra-thread-count",
        action="store",
        type=int,
        default=2,
        dest="infra_thread_count",
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


@pytest.hookimpl
def pytest_addhooks(pluginmanager: PytestPluginManager) -> None:
    from infrastructure.hookspecs import InfrastructureHookSpecs

    pluginmanager.add_hookspecs(InfrastructureHookSpecs)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if can_plugin_be_registered(config):
        infra_plugin = PytestValidate(config)
        config.pluginmanager.register(infra_plugin, INFRASTRUCTURE_PLUGIN_NAME)
        functions = config.pluginmanager.hook.pytest_infrastructure_collect_modifyitems(
            items=[]
        )
        infra_plugin.validate_infrastructure(functions)


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
        self.thread_count = config.getoption("infra_thread_count")

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

    def validate_infrastructure(self, functions: List[InfrastructureFunction]) -> None:
        ...

    @pytest.fixture
    def infra_functions(self) -> List[InfrastructureFunction]:
        return self._infrastructure_manager.get_applicable(self.environment)

    @pytest.hookimpl()
    def pytest_report_header(self, config: Config) -> str:
        if config.getoption("verbose") > 0:
            message = (
                "".join([fx.__name__ for fx in self._infrastructure_functions])
                or "In Infrastructure functions."
            )
            return message


def infrastructure(
    order: int = 0, ignored_envs: Optional[Set[str]] = None, isolated: bool = False
):
    """
    Bread and button of pytest-infrastructure.  Stores implementations of the decorator globally
    which are then available to the PytestValidate plugin to invoke and apply its custom logic to the pytest run.
    """

    def decorator(func):
        wrapper = InfrastructureFunction(
            real_function=func,
            order=order,
            ignored_envs=ignored_envs,
            isolated=isolated,
        )
        PytestValidate.register_wrapper_func(wrapper)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator
