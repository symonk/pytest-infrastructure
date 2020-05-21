# -*- coding: utf-8 -*-
from testing.testing_utils import get_sample_validate_file, get_path_to_test_file


def test_accessing_validation_file_fixture_without_cli_raises(testdir):
    testdir.makepyfile(
        """
        def test_validation_fx_exception_is_raised(validation_file):
            pass
    """
    )
    result = testdir.runpytest("-v")
    result.stdout.fnmatch_lines(["*ValidationFixtureException*"])
    assert result.ret == 1


def test_plugin_is_registered_without_bypass_flag(testdir, request):
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


def test_validation_fixture_is_passed_through(testdir, valid_file_one_func):
    testdir.makepyfile(
        """
        from testing.testing_utils import get_sample_validate_file

        def test_validation_file(validation_file):
            assert validation_file == get_sample_validate_file()
        """
    )
    assert testdir.runpytest(f"--infrastructure-file={valid_file_one_func}").ret == 0


def test_validate_function_can_be_collected_from_path(testdir):
    testdir.makepyfile(
        """
        def test_can_collect_validate_functions():
            pass

    """
    )
    file_for_arg = get_sample_validate_file()
    testdir.runpytest(f"--infrastructure-file={file_for_arg}")


def test_validate_raises(testdir):
    testdir.makepyfile(
        """
        def test_when_raises():
            pass

    """
    )
    file_for_raises = get_path_to_test_file("validate_raises.py")
    testdir.runpytest(f"--infrastructure-file={file_for_raises}")


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


def test_plugin_summary(testdir):
    testdir.makepyfile(
        """
        def test_summary(request):
            pass

    """
    )
    file = get_path_to_test_file("hybrid_mix_of_functions.py")
    assert testdir.runpytest(f"--infrastructure-file={file}").ret == 5


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


def test_pytest_xdist_slave_unregistered(testdir, valid_file_one_func):
    testdir.makepyfile(
        """
        import pytest
        @pytest.mark.parametrize("num", range(20))
        def test_paramed_data(request, num):
            plugin = request.config.pluginmanager.get_plugin('pytest_infrastructure')
            assert plugin is None
    """
    )
    result = testdir.runpytest("--infrastructure-file", valid_file_one_func, "-n=4")
    assert result.ret == 0
