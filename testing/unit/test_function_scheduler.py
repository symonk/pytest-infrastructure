from infrastructure.function_scheduler import FunctionScheduler
from infrastructure.decorators import infrastructure
from testing.testing_utils import build_dummy


def test_fs_parallel_results():
    fx = build_dummy(isolated=False)
    fs = FunctionScheduler(([fx], []), 1)
    fs.execute_functions()
    assert len(fs.results) == 1
    assert fs.results[0].fx == fx


def test_fs_none_data_sets():
    fs = FunctionScheduler(([], []), 1)
    fs.execute_functions()
    assert len(fs.results) == 0


def test_fs_parallel_raises():
    @infrastructure(isolated=False)
    def raises():
        raise Exception("raised in parallel!")

    fs = FunctionScheduler(([raises], []), 1)
    fs.execute_functions()
