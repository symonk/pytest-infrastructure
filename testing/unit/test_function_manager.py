from infrastructure import infrastructure
from infrastructure.function_manager import FunctionManager


@infrastructure()
def dummy():
    pass


def test_non_isolated_does_not_order_rewrite():
    dummy_func = dummy
    dummy.meta_data.order = -100
    fm = FunctionManager([dummy_func])
    fm.organize_functions()
    assert fm.parallel_functions[0].meta_data.order == -100


def test_negative_rewriting_isolated():
    dummy_func = dummy
    dummy.meta_data.order = -100
    dummy.meta_data.isolated = True
    fm = FunctionManager([dummy_func])
    fm.organize_functions()
    assert fm.isolated_functions[0].meta_data.order == 0
