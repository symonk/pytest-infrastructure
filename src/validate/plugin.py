# -*- coding: utf-8 -*-
import pytest
from _pytest.config import Config, hookspec

from validate.exceptions import ValidationFixtureException
from validate.strings import VALIDATION_FX_ERROR_MESSAGE


def pytest_addoption(parser):
    group = parser.getgroup("validate")
    group.addoption(
        "--validate-file",
        action="store",
        dest="validation_file",
        default=None,
        help="File path to your .py file which contains",
    )
    group.addoption(
        "--bypass-validation",
        action="store_false",
        dest="bypass_validation",
        default=True,
        help="Bypass the validation functions and execute testing without checking, disable the plugin completely",
    )


def pytest_configure(config: Config):
    if config.getoption("bypass_validation"):
        plugin = PytestValidate(config)
        config.pluginmanager.register(plugin, plugin.name)


@pytest.fixture
def validation_file(request):
    """
    Function scoped fixture to return the file path (if specified at runtime to --validation_file=
    If no file path is passed and this fixture has attempted use we will raise an exception, failing the test
    :param request: the dependency injected pytest request fixture
    :return: Optional[FileLike]
    """
    validation_file = request.config.option.validation_file
    if validation_file is not None:
        return request.config.option.validation_file
    else:
        raise ValidationFixtureException(VALIDATION_FX_ERROR_MESSAGE)


class PytestValidate:
    """
    The pytest validate plugin object;
    This plugin is only registered if the --bypass-validate arg is not provided, else it is completely skipped!
    """

    def __init__(self, config: Config):
        self.config = config
        self.name = "pytest_validate"

    @hookspec(historic=True)
    def pytest_plugin_registered(self, plugin, manager):
        if getattr(plugin, "name", None) == self.name:
            print(
                "pytest-validate has been registered, --bypass-validation was not passed"
            )
