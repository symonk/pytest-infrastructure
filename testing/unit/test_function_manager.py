from infrastructure.function_manager import FunctionManager
from testing.testing_utils import build_dummy


def test_non_isolated_does_not_order_rewrite():
    fm = FunctionManager([build_dummy(order=-100)])
    fm.organize_functions()
    assert fm.parallel_functions[0].meta_data.order == -100


def test_negative_rewriting_isolated():
    fm = FunctionManager([build_dummy(order=-100, isolated=True)])
    fm.organize_functions()
    assert fm.isolated_functions[0].meta_data.order == 0


def test_ordering_is_correct():
    fm = FunctionManager(
        [
            build_dummy(order=-1, isolated=True),
            build_dummy(order=1, isolated=True),
            build_dummy(order=150, isolated=True),
        ]
    )
    fm.organize_functions()
    assert fm.isolated_functions[0].meta_data.order == 0
    assert fm.isolated_functions[1].meta_data.order == 1
    assert fm.isolated_functions[2].meta_data.order == 150


def test_disabled_functions_are_removed():
    f1, f2, f3, f4, f5 = (
        build_dummy(order=-1, isolated=True, enabled=False),
        build_dummy(order=1, isolated=False, enabled=False),
        build_dummy(order=-10, isolated=True, not_on_env=["staging"]),
        build_dummy(order=-1000),
        build_dummy(order=-1000, isolated=True),
    )
    fm = FunctionManager([f1, f2, f3, f4, f5], environment="not-staging")
    fm.organize_functions()
    assert len(fm.disabled_functions) == 3
    assert fm.disabled_functions[0] == f1
    assert fm.disabled_functions[1] == f2
    assert fm.disabled_functions[2] == f3
    assert len(fm.isolated_functions) == 1
    assert len(fm.parallel_functions) == 1
    assert f4 in fm.parallel_functions
    assert f5 in fm.isolated_functions
