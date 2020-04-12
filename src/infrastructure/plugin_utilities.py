from colorama import Fore


def print_in_color(color, message):
    print(get_text_in_color(color, message))


def get_text_in_color(color, message):
    return f"{getattr(Fore, color.upper())} {message} {Fore.RESET}"
