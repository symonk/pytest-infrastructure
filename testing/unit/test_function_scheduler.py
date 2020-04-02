from infrastructure.function_scheduler import FunctionScheduler
from testing.testing_utils import build_dummy


def test_fs_parallel_results():
    fx = build_dummy(isolated=False)
    fs = FunctionScheduler(([fx], []), 1)
    fs.begin_workload()
    assert len(fs.parallel_results) == 1
    assert fs.parallel_results[0].fx == fx
