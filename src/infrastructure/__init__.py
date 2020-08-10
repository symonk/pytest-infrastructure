from colorama import init
from os import name
from .decorators import INFRASTRUCTURE_FUNCTIONS
from .decorators import infrastructure

if name == "nt":
    init(convert=True)


__all__ = [infrastructure, INFRASTRUCTURE_FUNCTIONS]