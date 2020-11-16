from _pytest.config import ExitCode


def test_sequential_only_order_is_ok(testdir):
    path = testdir.makepyfile(
        """
        from infrastructure import infrastructure

        @infrastructure(order=1)
        def one(): pass

        @infrastructure(order=2)
        def two(): pass

        @infrastructure(order=3)
        def three(): pass

        @infrastructure(order=4)
        def four(): pass

        @infrastructure(order=5)
        def five(): pass

        @infrastructure()
        def zero(): pass

        @infrastructure(order=-1)
        def disabled(): pass
        """
    )
    result = testdir.runpytest(f"--infra-module={path}")
    assert result.ret == ExitCode.NO_TESTS_COLLECTED
    result.stdout.fnmatch_lines(
        [
            "*zero*<Concurrent>*",
            "*one*<Sequential>*",
            "*two*<Sequential>*",
            "*three*<Sequential>*",
            "*four*<Sequential>*",
            "*five*<Sequential>*",
            "*disabled*<Disabled>*",
        ],
        consecutive=True,
    )
