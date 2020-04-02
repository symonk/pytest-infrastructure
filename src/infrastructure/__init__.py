import sys

from infrastructure._version import version as __version__
from infrastructure.strings import PLUGIN_NAME
from infrastructure.decorators import infrastructure
from loguru import logger

config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "<green>{thread.name: <25} | {function: ^30} | {line: >3}</green> | {message}",
            "colorize": True,
            "enqueue": True,
            "backtrace": True,
            "diagnose": True,
        },
        {"sink": f"{PLUGIN_NAME}.log", "serialize": True},
    ],
    "extra": {"user": "someone"},
}
logger.configure(**config)
logger.enable(PLUGIN_NAME)

__all__ = ["__version__", infrastructure, logger]
