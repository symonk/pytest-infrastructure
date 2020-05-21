import os

from colorama import Fore
from infrastructure.strings import GREEN


def print_in_color(color, message) -> None:
    """
    Print to stdout directly a coloured message
    :param color: the color that should be returned
    :param message: the message to encapsulate
    """
    print(get_text_in_color(color, message))


def get_text_in_color(color, message) -> str:
    """
    Get text in a particular color, used for pretty printing to standard out
    :param color: the color that should be returned
    :param message: the message to encapsulate
    :return: a string of the coloured message
    """
    return f"{getattr(Fore, color.upper())} {message} {Fore.RESET}"


def is_xdist_slave(config) -> bool:
    """
    xdist compatbility checks; only register the plugin on the master node when xdist is involved
    n.b -> worker / slaveinput should NOT run this plugin, this checks for xdist enablement and acts accordingly
    :return: a boolean indicating if the current invokation of pytest is on an xdist slave
    """
    return hasattr(config, "slaveinput")


def get_worker_id() -> str:
    return os.environ.get("PYTEST_XDIST_WORKER ", "Master")


def infra_print(message: str, color: str = GREEN) -> None:
    print(
        f"{get_worker_id()} - [pytest-infrastructure] {get_text_in_color(color, message)}",
        flush=True,
    )
