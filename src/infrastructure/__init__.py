import sys
import os

from loguru import logger
from .strings import INFRASTRUCTURE_PLUGIN_NAME
from .function_finder import InfrastructureFunctionFinder  # noqa
from .function_manager import FunctionManager  # noqa
from .function_scheduler import FunctionScheduler  # noqa

config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "pytest-infrastructure | {message}",
            "enqueue": True,
            "backtrace": True,
            "diagnose": True,
        },
        {
            "sink": f"pytest-infra{os.path.sep}{INFRASTRUCTURE_PLUGIN_NAME}-{os.getpid()}.log",
            "format": "pytest-infrastructure | {message}",
            "enqueue": True,
            "backtrace": True,
            "diagnose": True,
        },
    ]
}
logger.configure(**config)
logger.enable(INFRASTRUCTURE_PLUGIN_NAME)


__all__ = ["__version__", logger]
