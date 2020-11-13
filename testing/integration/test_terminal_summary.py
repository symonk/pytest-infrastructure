def test_terminal_summary_with_funcs(testdir) -> None:
    path = testdir.makepyfile(
        """
        from infrastructure import infrastructure

        @infrastructure(name='')
        def function_one(): pass

        @infrastructure()
        def function_two(): pass
        """
    )
    result = testdir.runpytest("-s", "-v", f"--infra-module={path}")
    result.stdout.fnmatch_lines(
        ["*pytest-infrastructure results*", "function_one: <*", "function_two: <*"]
    )


def test_terminal_summary_without_funcs(testdir) -> None:
    path = testdir.makepyfile(
        """
        def run_this():
            pass
        """
    )
    result = testdir.runpytest("-s", "-v", f"--infra-module={path}")
    result.stdout.fnmatch_lines(
        [
            "*pytest-infrastructure results*",
            "no pytest-infrastructure functions collected & executed.",
        ]
    )
