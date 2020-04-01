import sys

from infrastructure._version import version as __version__
from infrastructure.decorators import infrastructure
from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    format="<green>{thread.name: <25} | {function: ^30} | {line: >3}</green> | {message}",
    colorize=True,
    enqueue=True,
    backtrace=True,
)
new_level = logger.level("functions", no=38, color="<yellow>", icon="🐍")


__all__ = ["__version__", infrastructure, logger]
