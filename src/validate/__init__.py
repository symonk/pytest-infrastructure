import sys

from validate._version import version as __version__
from loguru import logger

logger.add("pytest_validate.log", rotation="500 MB")
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time}</green> <level>{message}</level>",
    enqueue=True,
)

__all__ = ["__version__", logger]
