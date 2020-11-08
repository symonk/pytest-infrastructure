from _pytest.config import ExitCode
from _pytest.pytester import Testdir


def test_terminal_summary_with_funcs(testdir: Testdir) -> None:
    testdir.makepyfile(
        """
        from infrastructure import infrastructure

        @infrastructure()
        def function_one(): pass

        @infrastructure()
        def function_two(): pass

        def test_this(infra_functions):
            print(infra_functions)
        """
    )
    result = testdir.runpytest("-s", "-v")
    assert result.ret == ExitCode.OK
    result.stdout.fnmatch_lines(
        [
            "------------------------ pytest-infrastructure results ------------------------",
            "function_one: <*",
            "function_two: <*",
        ]
    )


def test_terminal_summary_without_funcs(testdir: Testdir) -> None:
    result = testdir.runpytest("-s", "-v")
    assert result.ret == ExitCode.NO_TESTS_COLLECTED
    result.stdout.fnmatch_lines(
        [
            "------------------------ pytest-infrastructure results ------------------------",
            "no pytest-infrastructure functions collected & executed.",
        ]
    )
