from _pytest.config import ExitCode


def test_custom_name_is_ok(testdir):
    path = testdir.makepyfile(
        """
        from infrastructure import infrastructure

        @infrastructure(name="Bazinga!")
        def some_function():
            pass

        def test_something():
            pass
        """
    )
    result = testdir.runpytest(f"--infra-module={path}")
    assert result.ret == ExitCode.OK
    result.stdout.fnmatch_lines(["*Bazinga!*"])


def test_name_none(testdir):
    path = testdir.makepyfile(
        """
        from infrastructure import infrastructure

        @infrastructure(name=None)
        def some_function():
            pass

        def test_something():
            pass
        """
    )
    result = testdir.runpytest(f"--infra-module={path}")
    assert result.ret == ExitCode.OK
    result.stdout.fnmatch_lines(["*some_function*"])


def test_custom_name_empty_str(testdir):
    path = testdir.makepyfile(
        """
        from infrastructure import infrastructure

        @infrastructure(name="  ")
        def some_function():
            pass

        def test_something():
            pass
        """
    )
    result = testdir.runpytest(f"--infra-module={path}")
    assert result.ret == ExitCode.OK
    result.stdout.fnmatch_lines(["*some_function*"])
