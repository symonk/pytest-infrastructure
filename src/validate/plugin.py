# -*- coding: utf-8 -*-
import pytest
from validate.exceptions import ValidationFixtureException
from validate.function_finder import ValidateFunctionFinder
from validate.strings import VALIDATION_FX_ERROR_MESSAGE
from validate import logger


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
        help="Supress stdout message(s) from pytest validate"
    )
    group.addoption(
        "--validate-env",
        action="store",
        type=str,
        default="",
        help="Runtime environment; only_on_env= of validation functions will account for this" \
             "Note: if not specified, all validate functions will be executed."
    )


def pytest_configure(config):
    logger.info("Pytest validate has been loaded...doing initial checks")
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
    plugin = PytestValidate(config)
    if config.getoption("--bypass-validation"):
        config.pluginmanager.register(plugin, plugin.name)
        plugin.collect_validate_functions()
    else:
        logger.info(
            "Pytest validate will be deregistered because --bypass-validation was provided"
        )
        config.pluginmanager.unregister(plugin, plugin.name)


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

    def collect_validate_functions(self):
        logger.info(f"Pytest validate is collecting functions it can detect...")
        self.functions = ValidateFunctionFinder(
            self.file_path
        ).gather_validate_functions()
        if not self.functions:
            logger.info(f"No validation functions detected, plugin will unregister!")
            self.config.pluginmanager.unregister(self, self.name)

    def pytest_sessionstart(self):
        for function in self.functions:
            self._go_validate(function)

    @logger.catch
    def _go_validate(self, function):
        pass
