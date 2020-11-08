import pytest


@pytest.mark.skip(reason="need to rethink the auto-aware decorator")
def test_terminal_summary_with_funcs(testdir) -> None:
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
    result.stdout.fnmatch_lines(
        [
            "------------------------ pytest-infrastructure results ------------------------",
            "function_one: <*",
            "function_two: <*",
        ]
    )


@pytest.mark.skip(reason="need to rethink the auto-aware decorator")
def test_terminal_summary_without_funcs(testdir) -> None:
    result = testdir.runpytest("-s", "-v")
    result.stdout.fnmatch_lines(
        [
            "------------------------ pytest-infrastructure results ------------------------",
            "no pytest-infrastructure functions collected & executed.",
        ]
    )
