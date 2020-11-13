from _pytest.config import Config


def is_xdist_worker(config: Config) -> bool:
    """
    xdist worker check, the plugin workload is only carried out by the master process, this means:
    1) The initial process when running without xdist (-n)
    2) The master process (not a spawned execnet gateway worker node
    """
    return hasattr(config, "workerinput")


def can_plugin_be_registered(config: Config) -> bool:
    """
    Bundled checks for deciding if registering the plugin is sufficient.
    Accounts for the following:

     - is the --skip-infra CLI option provided
     - is the -h pytest help option provided
     - is pytest running in --co / --collect-only mode
     - is the executing process the true 'master' under both sequential & distributed setups.

     :param config: The pytest config object.
     :returns: A boolean indicating if the plugin should be registered or not.
    """
    do_not_skip = not config.getoption("skip_infra")
    not_collect_only = not config.getoption("collectonly")
    not_pytest_help = not config.getoption("help")
    is_master = not is_xdist_worker(config)
    has_function_module = config.getoption("infra_module") is not None
    return all(
        (do_not_skip, not_collect_only, not_pytest_help, is_master, has_function_module)
    )
