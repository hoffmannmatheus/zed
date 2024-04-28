from typing import Any

from colorama import Back, Fore, Style


def pprint(
    *args: Any,
    color: str = "",
    style: str = "",
    **kwargs: Any,
) -> None:
    color_str = Fore.RESET + Style.RESET_ALL + Back.RESET + color + style
    print(color_str, end="")
    print(*args, **kwargs, end="")
    print(Fore.RESET + Style.RESET_ALL + Back.RESET)


def pprint_error(*args: Any, **kwargs: Any) -> None:
    pprint(*args, **kwargs, color=Fore.RED)


def pprint_warn(*args: Any, **kwargs: Any) -> None:
    pprint(*args, **kwargs, color=Fore.YELLOW)


def pprint_success(*args: Any, **kwargs: Any) -> None:
    pprint(*args, **kwargs, color=Fore.GREEN)


def pprint_cyan(*args: Any, **kwargs: Any) -> None:
    pprint(*args, **kwargs, color=Fore.LIGHTCYAN_EX)


def pprint_dim(*args: Any, color: str = "", **kwargs: Any) -> None:
    pprint(*args, **kwargs, color=color, style=Style.DIM)


def color(text: str, color: str = "", style: str = "") -> str:
    return f"{color}{style}{text}{Fore.RESET}{Style.RESET_ALL}{Back.RESET}"
