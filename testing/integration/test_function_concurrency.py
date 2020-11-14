from _pytest.config import ExitCode


def test_parallel_executions(testdir) -> None:
    path = testdir.makepyfile(
        """
        from infrastructure import infrastructure
        from functools import partial

        @infrastructure()
        def one(): pass

        @infrastructure()
        def two(): pass

        @infrastructure()
        def three(): pass

        @infrastructure()
        def four(): pass

        @infrastructure()
        def five(): raise Exception('nope')

        def test_something():
            pass
        """
    )
    result = testdir.runpytest(f"--infra-module={path}")
    assert result.ret == ExitCode.OK
