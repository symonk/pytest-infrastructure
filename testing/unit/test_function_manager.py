import copy
from typing import List

from infrastructure import infrastructure
from infrastructure.function_manager import FunctionManager
import types


@infrastructure()
def dummy():
    pass


def copy_func(f):
    fn = types.FunctionType(
        f.__code__, f.__globals__, f.__name__, f.__defaults__, f.__closure__
    )
    # in case f was given attrs (note this dict is a shallow copy):
    fn.__dict__ = copy.deepcopy(f.__dict__)
    return fn


def build_dummy(
    order: int = None,
    enabled: bool = None,
    not_on_env: List = None,
    isolated: bool = None,
):
    fx = copy_func(dummy)
    if order is not None:
        fx.meta_data.order = order
    if enabled is not None:
        fx.meta_data.enabled = enabled
    if not_on_env is not None:
        fx.meta_data.not_on_env = [] or not_on_env
    if isolated is not None:
        fx.meta_data.isolated = isolated
    return fx


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
