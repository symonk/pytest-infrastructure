# -*- coding: utf-8 -*-

import pytest
from infrastructure.exceptions import ValidationFixtureException
from infrastructure.function_finder import FunctionFinder
from infrastructure.strings import (
    INFRASTRUCTURE_NO_FILE_PATH_OR_FUNCS_FOUND,
    INFRASTRUCTURE_FX_ERROR_MESSAGE,
    INFRASTRUCTURE_BYPASS_PROVIDED,
    INFRASTRUCTURE_COLLECTION_ONLY,
    INFRASTRUCTURE_XDIST_SLAVE,
    INFRASTRUCTURE_PLUGIN_NAME,
)

from infrastructure.function_manager import FunctionManager
from infrastructure.function_scheduler import FunctionScheduler


def pytest_addoption(parser):
    group = parser.getgroup(INFRASTRUCTURE_PLUGIN_NAME)
    group.addoption(
        "--infrastructure-file",
        action="store",
        type=str,
        help="File path to your .py file which contains infrastructure functions",
    )
    group.addoption(
        "--bypass-validation",
        action="store_false",
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
    main_plugin = PytestValidate(config)
    config.pluginmanager.register(main_plugin, main_plugin.name)


@pytest.fixture
def validation_file(request):
    """
    Function scoped fixture to return the file path (if specified at runtime to --validation-file=
    If no file path is passed and this fixture has attempted use we will raise an exception, failing the test
    :param request: the dependency injected pytest request fixture
    :return: Optional[FileLike]
    """
    validation_file = request.config.getoption("--infrastructure-file")
    if validation_file:
        return validation_file
    else:
        raise ValidationFixtureException(INFRASTRUCTURE_FX_ERROR_MESSAGE)


class PytestValidate:
    """
    The pytest infrastructure plugin object;
    This plugin is only registered if the --bypass-infrastructure arg is not provided, else it is completely skipped!
    """

    def __init__(self, config):
        self.config = config
        self.name = "pytest_infrastructure"
        self.unfiltered_functions = None
        self.file_path = self.config.getoption("--infrastructure-file")
        self.environment = config.getoption("--infrastructure-env")
        self.thread_count = config.getoption("--infrastructure-thread-count")

    @pytest.mark.tryfirst
    def pytest_configure(self):
        print("Pytest-infrastructure is checking if it is allowed to run...")
        if not self.config.getoption("--bypass-validation"):
            self._unregister(INFRASTRUCTURE_BYPASS_PROVIDED)
            return
        if self._is_xdist_slave():
            self._unregister(INFRASTRUCTURE_XDIST_SLAVE)
            return
        if self.config.getoption("collectonly"):
            self._unregister(INFRASTRUCTURE_COLLECTION_ONLY)
            return
        self.collect_validate_functions()

    def collect_validate_functions(self):
        print(
            f"Pytest-infrastructure is scanning for @infrastructure functions in {self.file_path}"
        )
        self.unfiltered_functions = FunctionFinder(
            self.file_path
        ).gather_infrastructure_functions()
        if not self.unfiltered_functions:
            self._unregister(INFRASTRUCTURE_NO_FILE_PATH_OR_FUNCS_FOUND)
        else:
            self.validate()

    def validate(self) -> None:
        """
        This is validates bread and butter; it is responsible for executing the functions in a controlled fashion
        in-line with the meta data of the particular function(s)
        """
        manager = FunctionManager(self.unfiltered_functions, self.environment)
        manager.organize_functions()
        scheduler = FunctionScheduler(
            (manager.isolated_functions, manager.parallel_functions), self.thread_count
        )
        scheduler.execute_functions()
        scheduler.report_summary()

    def _is_xdist_slave(self) -> bool:
        """
        xdist compatability checks; only register the plugin on the master node when xdist is involved
        n.b -> worker / slaveinput should NOT run this plugin, this checks for xdist enablement and acts accordingly
        :return: a boolean indicating if the current invokation of pytest is on an xdist slave
        """
        return hasattr(self.config, "slaveinput")

    def _unregister(self, reason: str):
        print(f"pytest-infrastructure will unregister the plugin because: {reason}")
        self.config.pluginmanager.unregister(self, self.name)
