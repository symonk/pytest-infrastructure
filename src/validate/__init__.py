import logging
from validate._version import version as __version__
from validate.decorators import validate

logger = logging.getLogger("validate")
file_handler = logging.FileHandler("mylog.log")
formatter = logging.Formatter(
    "[%(thread)d] %(asctime)s : %(levelname)s : %(name)s ==> %(message)s"
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

__all__ = ["__version__", validate]
