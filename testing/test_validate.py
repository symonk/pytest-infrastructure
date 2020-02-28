# -*- coding: utf-8 -*-


def test_accessing_validation_file_fixture_without_cli_raises(testdir):
    testdir.makepyfile(
        """
        def test_validation_file_none(validation_file):
            print(validation_file)
    """
    )

    result = testdir.runpytest("-v")
    result.stdout.fnmatch_lines(["*ValidationFixtureException*"])
    assert result.ret == 1


def test_plugin_is_registered_without_bypass_flag(testdir, request):
    plugin_manager = request.config.pluginmanager
    assert plugin_manager.is_registered(plugin_manager.get_plugin("pytest_validate"))


def test_plugin_is_not_registered_with_bypass_flag(testdir):
    testdir.makepyfile(
        """
        def test_with_bypass_validate(request):
            plugin_manager = request.config.pluginmanager
            assert not plugin_manager.is_registered(
                plugin_manager.get_plugin("pytest_validate")
            )
    """
    )
    assert testdir.runpytest("--bypass-validation").ret == 0
