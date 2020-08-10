# -*- coding: utf-8 -*-
import os
from dataclasses import dataclass

import pytest
from infrastructure.exceptions import ValidationFixtureException
from infrastructure.plugin_utilities import is_xdist_slave
from infrastructure.plugin_utilities import infra_print
from infrastructure.strings import INFRASTRUCTURE_FX_ERROR_MESSAGE
from infrastructure.strings import INFRASTRUCTURE_PLUGIN_NAME
from infrastructure import INFRASTRUCTURE_FUNCTIONS

from infrastructure.function_manager import FunctionManager
from infrastructure.function_scheduler import FunctionScheduler


def pytest_addoption(parser):
    group = parser.getgroup(INFRASTRUCTURE_PLUGIN_NAME)
    group.addoption(
        "--bypass-validation",
        action="store_true",
        help="Bypass the validation functions and execute testing without checking, disable the plugin completely",
    )
    group.addoption(
        "--infrastructure-thread-count",
        action="store",
        type=int,
        default=2,
        help="If specified will use threads to execute infrastructure threads in parallel",
    )
    group.addoption(
        "--infrastructure-env",
        action="store",
        type=list,
        help="Runtime environment; only_on_env= of validation functions will account for this"
        "Note: if not specified, all infrastructure functions will be executed.",
    )


@pytest.mark.tryfirst
def pytest_configure(config):
    infra_print("welcome to pytest-infrastructure... scanning for disabling flags")
    disallowed, reason = _is_unsafe_to_register(config)
    if disallowed:
        infra_print(f"not loaded because: {reason}")
        return
    infra_print("has been successfully loaded")
    main_plugin = PytestValidate(config)
    config.pluginmanager.register(main_plugin, main_plugin.name)


@dataclass(repr=True)
class ReasonContainer:
    collect_only: bool
    pytest_help: bool
    xdist_slave: bool
    bypass_provided: bool

    def disallowed(self) -> tuple:
        """
        Check if any of the checks have been met in order to not register the plugin
        Any one of these is valid enough that the plugin should NOT be loaded.
        In the instance where the checks fail, it will provide a nice message to stdout to explain why
        :return: a boolean indicating the state
        """
        return (
            any(
                (
                    self.collect_only,
                    self.pytest_help,
                    self.xdist_slave,
                    self.bypass_provided,
                )
            ),
            repr(self),
        )


def _is_unsafe_to_register(config) -> tuple:
    """
    Return a boolean value indicating if the plugin should be registered or not.
    :param config: the pytest config object
    :return: boolean if the plugin should be registered or not
    """
    collect_only = config.getoption("collectonly")
    pytest_help = config.getoption("help")
    xdist_slave = is_xdist_slave(config)
    bypass_provided = config.getoption("--bypass-validation")
    return ReasonContainer(
        collect_only, pytest_help, xdist_slave, bypass_provided
    ).disallowed()


class PytestValidate:
    """
    The pytest infrastructure plugin object;
    This plugin is only registered if the --bypass-infrastructure arg is not provided, else it is completely skipped!
    """

    def __init__(self, config):
        self.config = config
        self.name = "pytest_infrastructure"
        self.functions = None
        self.environment = config.getoption("--infrastructure-env")
        self.thread_count = config.getoption("--infrastructure-thread-count")

    def collect_validate_functions(self):
        infra_print(
            "plugin permitted, collecting @infrastructure "
            f"functions now..."
        )
        self.functions = INFRASTRUCTURE_FUNCTIONS
        self.validate()

    def validate(self) -> None:
        """
        This is validates bread and butter; it is responsible for executing the functions in a controlled fashion
        in-line with the meta data of the particular function(s)
        """
        manager = FunctionManager(self.functions, self.environment)
        manager.organize_functions()
        scheduler = FunctionScheduler(
            (manager.isolated_functions, manager.parallel_functions), self.thread_count
        )
        scheduler.execute_functions()
        scheduler.report_summary()
