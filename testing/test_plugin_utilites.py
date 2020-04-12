from infrastructure.plugin_utilities import print_in_color
from infrastructure.plugin_utilities import get_text_in_color


def test_plugin_utilities(capfd):
    print_in_color("GREEN", "This is my message")
    captured = capfd.readouterr()
    assert "\x1b[32m This is my message \x1b[39m\n" in captured.out


def test_get_text():
    text = get_text_in_color("green", 'This is my message')
    assert text == "\x1b[32m This is my message \x1b[39m"
