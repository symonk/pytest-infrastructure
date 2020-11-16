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
        ["*pytest-infrastructure results*", "*function_one*", "*function_two*"]
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


def test_meta_data_accuracy(testdir):
    # TODO TEST THIS WITH PROCESSES, ITS NOT PICKELABLE ATM!
    path = testdir.makepyfile(
        """
        from infrastructure import infrastructure

        @infrastructure()
        def do_it(): pass
        """
    )
    result = testdir.runpytest(
        f"--infra-module={path}",
        "--max-workers=10",
        "--infra-env=staging",
        "--soft-validate",
    )
    result.stdout.fnmatch_lines(
        [
            "ExecutionMetaData*soft_run=True, infra_environment='staging', max_workers=10, use_processes=False*"
        ]
    )
