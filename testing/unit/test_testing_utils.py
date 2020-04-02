import pytest
from testing.testing_utils import get_path_to_test_file


def test_sample_file_no_file():
    with pytest.raises(FileNotFoundError):
        get_path_to_test_file("fail.py")
