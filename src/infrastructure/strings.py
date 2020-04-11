INFRASTRUCTURE_PLUGIN_NAME = "pytest-infrastructure"
INFRASTRUCTURE_XDIST_SLAVE = "pytest-infrastructure does not run on xdist slave nodes"
INFRASTRUCTURE_BYPASS_PROVIDED = "--bypass-validation was specified on CLI"
INFRASTRUCTURE_COLLECTION_ONLY = "--collect-only was specified on the CLI"
INFRASTRUCTURE_NO_FILE_PATH_OR_FUNCS_FOUND = (
    "No --validation-file passed or no @infrastructure functions found"
)
INFRASTRUCTURE_FX_ERROR_MESSAGE = (
    "Attempted to access the validation_file fixture without specifying "
    "a --validation_file"
)
