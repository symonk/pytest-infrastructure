from infrastructure import InfrastructureFunctionFinder
from testing.testing_utils import get_path_to_test_file


def test_no_file():
    finder = InfrastructureFunctionFinder(
        get_path_to_test_file("one_validate_function.py")
    )
    assert len(finder.gather_infrastructure_functions()) == 1


def test_multiple_functions():
    finder = InfrastructureFunctionFinder(
        get_path_to_test_file("no_validate_functions.py")
    )
    assert len(finder.gather_infrastructure_functions()) == 0


def test_non_annotated_functions():
    finder = InfrastructureFunctionFinder(
        get_path_to_test_file("non_annotated_functions.py")
    )
    assert len(finder.gather_infrastructure_functions()) == 0
