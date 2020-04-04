from infrastructure import FunctionScheduler
from testing.testing_utils import build_dummy


def test_fs_parallel_results():
    fx = build_dummy(isolated=False)
    fs = FunctionScheduler(([fx], []), 1)
    fs.execute_functions()
    assert len(fs.parallel_results) == 1
    assert fs.parallel_results[0].fx == fx


def test_fs_none_data_sets():
    fs = FunctionScheduler(([], []), 1)
    fs.execute_functions()
    assert len(fs.parallel_results) == 0
    assert len(fs.isolated_results) == 0
