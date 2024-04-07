from simple_term_menu import TerminalMenu
from process_data import minutes_from_str


def prompt(options, title):
    terminal_menu = TerminalMenu(options, title=title)
    result = None
    while result is None:
        result = terminal_menu.show()

    return options[result]


def prompt_many(options, title):
    terminal_menu = TerminalMenu(
        options,
        multi_select=True,
        show_multi_select_hint=True,
        multi_select_empty_ok=False,
        title=title,
    )
    terminal_menu.show()

    return [options[idx] for idx in terminal_menu.chosen_menu_indices]


def prompt_many_dict(options_dict: dict, title: str):
    selected = prompt_many(list(options_dict.keys()), title)
    return [options_dict[option] for option in selected]


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
