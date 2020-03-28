import os

from __project_root__ import ROOT_DIR


def get_path_to_test_file(file_name: str) -> str:
    test_file = os.path.join(ROOT_DIR, "testing", "test_data_files", file_name)
    if os.path.exists(test_file):
        return test_file
    else:
        raise FileNotFoundError(file_name)


def get_sample_validate_file():
    return get_path_to_test_file("one_validate_function.py")
