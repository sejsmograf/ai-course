from simple_term_menu import TerminalMenu
from process_data import minutes_from_str


def prompt(options, title):
    result = None
    while result is None:
        terminal_menu = TerminalMenu(options, title=title)
        result = terminal_menu.show()

    return options[result]


def prompt_dict(options_dict: dict, title: str):
    selected = prompt(list(options_dict.keys()), title)
    return options_dict[selected]


def prompt_time(prompt_str: str) -> int:
    options: list[str] = [f"{h:02d}:{m:02d}" for h in range(24) for m in range(60)]
    time_str: str = prompt(options, prompt_str) + ":00"

    hour: int = int(time_str[:2])
    if int(time_str[:2]) < 4:
        time_str = str(hour + 24) + time_str[2:]

    return minutes_from_str(time_str)
