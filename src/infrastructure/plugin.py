# -*- coding: utf-8 -*-
import functools
from dataclasses import dataclass
from typing import List, Set, Optional, Callable

import pytest
from _pytest.config import PytestPluginManager

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
        config.pluginmanager.register(PytestValidate(config), "pytest-infrastructure")
        functions = config.pluginmanager.hook.pytest_infrastructure_collect()
        config.pluginmanager.hook.pytest_infrastructure_validate(functions=functions)


class PytestValidate:
    """
    The pytest infrastructure plugin object;
    This plugin is only registered if the --bypass-infrastructure arg is not provided, else it is completely skipped!
    """

    infrastructure_functions: List[Callable] = []

    def __init__(self, config):
        self.config = config
        self.functions = None
        self.environment = config.getoption("infra_env")
        self.thread_count = config.getoption("infra_thread_count")

    @pytest.hookimpl
    def infrastructure_collect(self) -> List[Callable]:
        ...

    @pytest.hookimpl
    def infrastructure_validate(self, functions: List[Callable]) -> None:
        ...


@dataclass(frozen=True, repr=True)
class InfraArgs:
    """
    Simple argument class that should be provided to the @infrastructure decorator.
    for example:
        @infrastructure(InfraArgs(order=10, active=False, ignored_on_env={'staging'}, isolated=True)
        def some_function() -> None:
            ...
        order: A 'priority' indicator, where lower is higher priority.
        active: If the decorated function is applicable for collection & execution
        ignored_on_env: Set of environments that the function will not be validated again (--infra-env)
        isolated: If the function should be sequentially run (after threaded functions) in isolation.
    """

    order: int = 0
    active: bool = True
    ignored_on_env: Optional[Set[str]] = None
    isolated: bool = False


def infrastructure(infra_args: InfraArgs):
    """
    Bread and button of pytest-infrastructure.  Stores implementations of the decorator globally
    which are then available to the PytestValidate plugin to invoke and apply its custom logic to the pytest run.
    """

    def decorator(func):
        PytestValidate.infrastructure_functions.append(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            return wrapper

        return decorator
