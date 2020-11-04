from unittest.mock import Mock

from _pytest.config import Config
from _pytest.monkeypatch import MonkeyPatch

from infrastructure.utils.plugin_utilities import can_plugin_be_registered


def test_plugin_register_help(pytestconfig: Config, monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(pytestconfig.option, "help", True)
    assert not can_plugin_be_registered(pytestconfig)


def test_plugin_register_collect(
    pytestconfig: Config, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.setattr(pytestconfig.option, "collectonly", True)
    assert not can_plugin_be_registered(pytestconfig)


def test_plugin_register_xdist(pytestconfig: Config, monkeypatch: MonkeyPatch) -> None:
    pytestconfig.workerinput = []
    assert not can_plugin_be_registered(pytestconfig)
