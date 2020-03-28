from src.validate.decorators import validate
import logging

logger = logging.getLogger("validate")


@validate()
def validate_function_one():
    logger.info("executing the validate function")
