import pytest
from _pytest.config import ExitCode


@pytest.mark.parametrize(
    "infra_name, expected", [("Bazinga!", "Bazinga!"), (None, "test_it")]
)
def test_function_custom_name_options(testdir, infra_name, expected):
    resolved_name = "'{0}'".format(infra_name) if infra_name is not None else None
    path = testdir.makepyfile(
        f"""
        from infrastructure import infrastructure

        @infrastructure(name={resolved_name})
        def test_it():
            pass
        """
    )
    result = testdir.runpytest(f"--infra-module={path}")
    assert result.ret == ExitCode.OK
    result.stdout.fnmatch_lines([f"{expected}*"])
