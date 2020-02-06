# -*- coding: utf-8 -*-

import pytest

from src.validate.exceptions import ValidationFixtureException
from strings import VALIDATION_FX_ERROR_MESSAGE


def pytest_addoption(parser):
    group = parser.getgroup('validate')
    group.addoption(
        '--validate-file',
        action='store',
        dest='validation_file',
        default=None,
        help='File path to your .py file which contains'
    )
    group.addoption(
        '--bypass-validation',
        action='store_false',
        dest='bypass_validation',
        default=True,
        help='Bypass the validation functions and execute tests without checking'
    )


@pytest.fixture
def validation_file(request):
    """
    Function scoped fixture to return the file path (if specified at runtime to --validation_file=
    If no file path is passed and this fixture has attempted use we will raise an exception, failing the test
    :param request: the dependency injected pytest request fixture
    :return: Optional[FileLike]
    """
    validation_file = request.config.option.validation_file
    if not validation_file:
        return request.config.option.validation_file
    else:
        raise ValidationFixtureException(VALIDATION_FX_ERROR_MESSAGE)
