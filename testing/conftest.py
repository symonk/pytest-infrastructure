import pytest
from .testing_utils import get_path_to_test_file

pytest_plugins = "pytester"


@pytest.fixture
def valid_file_one_func():
    return get_path_to_test_file("one_validate_function.py")
