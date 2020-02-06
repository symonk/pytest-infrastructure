# -*- coding: utf-8 -*-


def test_accessing_validation_file_fixture_without_cli_raises(testdir):

    testdir.makepyfile(
        """
        def test_validation_file_none(validation_file):
            pass
    """
    )

    result = testdir.runpytest("-v")
    breakpoint()
    result.stdout.fnmatch_lines(["*::test_sth PASSED*"])

    assert result.ret == 1
