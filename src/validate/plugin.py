# -*- coding: utf-8 -*-
import pytest
from validate.exceptions import ValidationFixtureException
from validate.function_finder import ValidateFunctionFinder
from validate.strings import (
    VALIDATION_FX_ERROR_MESSAGE,
    VALIDATE_NO_FILE_PATH_OR_NO_FUNCTIONS_FOUND,
    VALIDATE_XDIST_SLAVE_OR_BYPASS_PROVIDED,
)

from validate import logger

from validate.function_manager import FunctionManager
from validate.function_scheduler import FunctionScheduler


def pytest_addoption(parser):
    group = parser.getgroup("validate")
    group.addoption(
        "--validate-file",
        action="store",
        default=None,
        help="File path to your .py file which contains validate functions",
    )
    group.addoption(
        "--bypass-validation",
        action="store_false",
        help="Bypass the validation functions and execute testing without checking, disable the plugin completely",
    )
    group.addoption(
        "--validate-thread-count",
        action="store",
        type=int,
        default=0,
        help="If specified will use threads to execute validate threads in parallel",
    )
    group.addoption(
        "--validate-silent",
        action="store_true",
        help="Supress stdout message(s) from pytest validate",
    )
    group.addoption(
        "--validate-env",
        action="store",
        type=str,
        default="",
        help="Runtime environment; only_on_env= of validation functions will account for this"
        "Note: if not specified, all validate functions will be executed.",
    )


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
    validation_file = request.config.getoption("--validate-file")
    if validation_file:
        return validation_file
    else:
        raise ValidationFixtureException(VALIDATION_FX_ERROR_MESSAGE)


class PytestValidate:
    """
    The pytest validate plugin object;
    This plugin is only registered if the --bypass-validate arg is not provided, else it is completely skipped!
    """

    def __init__(self, config):
        self.config = config
        self.name = "pytest_validate"
        self.functions = None
        self.file_path = self.config.getoption("--validate-file")
        self.silently = config.getoption("--validate-silent")
        self.environment = config.getoption("--validate-env")

    def pytest_configure(self):
        logger.info(
            r"""
        **********************************************************************
          ____        _            _    __     __    _ _     _       _
         |  _ \ _   _| |_ ___  ___| |_  \ \   / /_ _| (_) __| | __ _| |_ ___
         | |_) | | | | __/ _ \/ __| __|  \ \ / / _` | | |/ _` |/ _` | __/ _ \
         |  __/| |_| | ||  __/\__ \ |_    \ V / (_| | | | (_| | (_| | ||  __/
         |_|    \__, |\__\___||___/\__|    \_/ \__,_|_|_|\__,_|\__,_|\__\___|
                |___/
        **********************************************************************"""
        )
        logger.info("Pytest-validate is checking if it is allowed to run...")
        if (
            not self.config.getoption("--bypass-validation")
            or self._is_xdist_slave()
            or self.config.getoption("--collect-only")
        ):
            self._unregister(VALIDATE_XDIST_SLAVE_OR_BYPASS_PROVIDED)
        else:
            self.collect_validate_functions()

    def collect_validate_functions(self):
        logger.info(
            f"Pytest-validate is scanning for @validate functions in {self.file_path}"
        )
        self.functions = ValidateFunctionFinder(
            self.file_path
        ).gather_validate_functions()
        if not self.functions:
            self._unregister(VALIDATE_NO_FILE_PATH_OR_NO_FUNCTIONS_FOUND)
        else:
            logger.info(
                f"Pytest-validate found a total of {len(self.functions)} function(s); these are displayed below"
            )
            self.validate()

    def validate(self) -> None:
        """
        This is validates bread and butter; it is responsible for executing the functions in a controlled fashion
        in-line with the meta data of the particular function(s)
        """
        manager = FunctionManager(self.functions, self.environment)
        manager.organize_functions()
        scheduler = FunctionScheduler(manager.yield_usable_functions())
        scheduler.begin_workload()

    def _is_xdist_slave(self) -> bool:
        """
        xdist compatability checks; only register the plugin on the master node when xdist is involved
        n.b -> worker / slaveinput should NOT run this plugin, this checks for xdist enablement and acts accordingly
        :return: a boolean indicating if the current invokation of pytest is on an xdist slave
        """
        return hasattr(self.config, "slaveinput")

    def _unregister(self, reason: str):
        logger.info(f"pytest-validate will unregister the plugin because: {reason}")
        self.config.pluginmanager.unregister(self, self.name)
