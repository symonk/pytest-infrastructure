from sys import stdout
from infrastructure._version import version as __version__
from infrastructure.decorators import validate
from loguru import logger

logger.add(stdout, colorize=True, enqueue=True, backtrace=True)
new_level = logger.level("functions", no=38, color="<yellow>", icon="🐍")


__all__ = ["__version__", validate, logger]