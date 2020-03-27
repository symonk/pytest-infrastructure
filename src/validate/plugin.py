# -*- coding: utf-8 -*-
import pytest
from validate.exceptions import ValidationFixtureException
from validate.pathfinder import ValidateFunctionFinder
from validate.strings import VALIDATION_FX_ERROR_MESSAGE


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
        "--validate-env",
        action="store",
        help="Environment file to execute validate functions dynamically at runtime",
    )
    group.addoption(
        "--validate-thread-count",
        action="store",
        type=int,
        default=0,
        help="If specified will use threads to execute validate threads in parallel",
    )


def pytest_configure(config):
    plugin = PytestValidate(config)
    if config.getoption("--bypass-validation"):
        plugin.collect_validate_functions()
    else:
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
        self.name = "validate"
        self.functions = None
        self.file_path = self.config.getoption("--validate-file")
        self.validate_finder = ValidateFunctionFinder(self.file_path)

    def pytest_plugin_registered(self, plugin):
        if getattr(plugin, "name", None) == self.name:
            print(
                "pytest-validate has been registered, --bypass-validation was not passed"
            )

    def collect_validate_functions(self):
        self.functions = self.validate_finder.gather_validate_functions()
