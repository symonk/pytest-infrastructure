import pytest
from infrastructure.utils.import_utilities import import_module_from_path


def test_can_find_real_module(testdir) -> None:
    path = testdir.makepyfile("import os")
    module = import_module_from_path(path)
    assert "os" in dir(module)


def test_cannot_import_no_such_file(testdir) -> None:
    with pytest.raises(FileNotFoundError):
        path = testdir.makepyfile("import os").join("madeup.py")
        import_module_from_path(path)
