from validate import validate
from validate import logger


@validate()
def validate_function_one():
    logger.info("executing the infrastructure function")
