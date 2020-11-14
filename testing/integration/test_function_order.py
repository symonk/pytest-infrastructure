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
    result.stdout.re_match_lines(
        [
            "zero: * | Status: <Concurrent>",
            "one: * | Status: <Sequential>",
            "two: * | Status: <Sequential>",
            "three: * | Status: <Sequential>",
            "four: * | Status: <Sequential>",
            "five: * | Status: <Sequential>",
            "disabled: * | Status: <Disabled>",
        ],
        consecutive=True,
    )
