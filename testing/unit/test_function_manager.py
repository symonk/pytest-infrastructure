from infrastructure import infrastructure
from infrastructure.function_manager import FunctionManager


@infrastructure()
def dummy():
    pass


def build_dummy(
    order: int = None,
    enabled: bool = None,
    only_on_env: str = None,
    isolated: bool = None,
):
    fx = dummy
    if order is not None:
        fx.meta_data.order = order
    if enabled is not None:
        fx.meta_data.enabled = enabled
    if only_on_env is not None:
        fx.meta_data.only_on_env = only_on_env
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
            build_dummy(order=3, isolated=True),
        ]
    )
    fm.organize_functions()
    # TODO figure out how to stop all functions being the same reference!
