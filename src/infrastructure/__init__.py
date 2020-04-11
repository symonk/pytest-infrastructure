from loguru import logger
from .strings import PLUGIN_NAME
from .function_finder import InfrastructureFunctionFinder  # noqa
from .function_manager import FunctionManager  # noqa
from .function_scheduler import FunctionScheduler  # noqa

config = {
    "handlers": [
        {
            "sink": f"{PLUGIN_NAME}.log",
            "format": "pytest-infrastructure | {message}",
            "enqueue": True,
            "backtrace": True,
            "diagnose": True,
        }
    ]
}
logger.configure(**config)
logger.enable(PLUGIN_NAME)


__all__ = ["__version__", logger]
