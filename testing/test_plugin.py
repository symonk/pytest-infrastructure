# -*- coding: utf-8 -*-


def test_plugin_is_registered_without_bypass_flag(request):
    plugin_manager = request.config.pluginmanager
    assert plugin_manager.is_registered(plugin_manager.get_plugin("infrastructure"))


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


def test_thread_count_default(testdir):
    testdir.makepyfile(
        """
        def test_when_raises(request):
            assert request.config.getoption('--infrastructure-thread-count') == 2

    """
    )
    assert testdir.runpytest().ret == 0


def test_thread_count_override(testdir):
    testdir.makepyfile(
        """
        def test_when_raises(request):
            assert request.config.getoption('--infrastructure-thread-count') == 10

    """
    )
    assert testdir.runpytest("--infrastructure-thread-count=10").ret == 0


def test_collect_only_unregistered(testdir):
    testdir.makepyfile(
        """
        def test_dummy():
            pass
    """
    )
    result = testdir.runpytest("--collect-only")
    result.stdout.fnmatch_lines(
        [
            "*ReasonContainer(collect_only=True, pytest_help=False, xdist_slave=False, bypass_provided=False)*"
        ]
    )

