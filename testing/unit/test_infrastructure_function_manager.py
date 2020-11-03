from infrastructure.infrastructure_functions import (
    InfrastructureFunctionManager,
    InfrastructureFunction,
)


def dummy():
    pass


def test_retrieve_isolated_works_():
    isolated = InfrastructureFunction(dummy, order=10, isolated=True)
    mgr = InfrastructureFunctionManager().register(isolated)
    assert len(mgr.get_squashed()) == 1
    assert len(mgr.get_threaded()) == 0
    assert len(mgr.get_isolated()) == 1


def test_retrieve_threaded_works():
    threaded = InfrastructureFunction(dummy, order=1)
    mgr = InfrastructureFunctionManager().register(threaded)
    assert len(mgr.get_squashed()) == 1
    assert len(mgr.get_threaded()) == 1
    assert len(mgr.get_isolated()) == 0
