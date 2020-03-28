import os
from validate._version import version as __version__
from validate.decorators import validate
from loguru import logger

logger.add(
    f"logs{os.path.sep}logger.log",
    colorize=True,
    format="<green>{time}</green> <level>{message}</level>",
    backtrace=True,
    enqueue=True,
    serialize=False,
)
new_level = logger.level("validate_functions", no=38, color="<yellow>", icon="🐍")


__all__ = ["__version__", validate, logger]
