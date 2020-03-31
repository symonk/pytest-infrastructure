from infrastructure import validate
from infrastructure import logger


@validate()
def validate_function_one():
    logger.info("executing the infrastructure function")
