from infrastructure.utils.constants import INFRASTRUCTURE_PLUGIN_NAME


def test_when_collect_only_no_plugin_is_registered(testdir) -> None:
    result = testdir.runpytest("--co")
    plugins_dict = result.reprec._pluginmanager._name2plugin
    assert INFRASTRUCTURE_PLUGIN_NAME not in plugins_dict


def test_when_help_no_plugin_is_registered(testdir) -> None:
    result = testdir.runpytest("-h")
    plugins_dict = result.reprec._pluginmanager._name2plugin
    assert INFRASTRUCTURE_PLUGIN_NAME not in plugins_dict


def test_when_bypassed_infra_no_plugin_is_registered(testdir) -> None:
    result = testdir.runpytest("--skip-infra")
    plugins_dict = result.reprec._pluginmanager._name2plugin
    assert INFRASTRUCTURE_PLUGIN_NAME not in plugins_dict


def test_plugin_registered_by_default(testdir) -> None:
    result = testdir.runpytest(f"--infra-module={testdir.makepyfile('')}")
    plugins_dict = result.reprec._pluginmanager._name2plugin
    assert INFRASTRUCTURE_PLUGIN_NAME in plugins_dict
