import os
from typing import List

from infrastructure import infrastructure
import types
import copy
from __project_root__ import ROOT_DIR


def get_path_to_test_file(file_name: str) -> str:
    test_file = os.path.join(ROOT_DIR, "testing", "test_data_files", file_name)
    if os.path.exists(test_file):
        return test_file
    else:
        raise FileNotFoundError(file_name)


def get_sample_validate_file():
    return get_path_to_test_file("one_validate_function.py")


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
