from functools import partial
from typing import Type

import pytest
from infrastructure import InfrastructureFunction
from infrastructure.function_management import InfrastructureFunctionManager

pytest_plugins = "pytester"


@pytest.fixture()
def manager_cls() -> Type[InfrastructureFunctionManager]:
    """
    Function scoped callable function manager, can be passed an optional list of functions.
    """
    return InfrastructureFunctionManager


@pytest.fixture()
def manager(manager_cls) -> InfrastructureFunctionManager:
    """
    Function scoped instance of the function manager without any functions loaded.
    """
    return manager_cls()


@pytest.fixture()
def dummy_callable() -> partial:
    """
    Function scoped dummy function, passable into the manager for registration.
    """
    return partial(InfrastructureFunction, executable=lambda x: x)
