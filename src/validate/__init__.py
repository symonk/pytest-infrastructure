import os
import sys
from validate._version import version as __version__
from validate.decorators import validate
from loguru import logger

logger.add(
    colorize=True,
    enqueue=True,
)
new_level = logger.level("functions", no=38, color="<yellow>", icon="🐍")


__all__ = ["__version__", validate, logger]
