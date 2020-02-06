

class ValidationFixtureException(Exception):
    """
    Custom exception raised when attempting to use fixture of pytest-validation when no --validation-file is set
    """
    pass
