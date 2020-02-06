# -*- coding: utf-8 -*-


def test_accessing_validation_file_fixture_without_cli_raises(testdir):

    testdir.makepyfile(
        """
        def test_validation_file_none(validation_file):
            print(validation_file)
    """
    )

    result = testdir.runpytest("-v")
    result.stdout.fnmatch_lines(["*ValidationFixtureException*"])
    assert result.ret == 1
