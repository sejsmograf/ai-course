import sys
import time
from functools import wraps
from typing import NamedTuple, Optional, Callable
from process_data.utils import minutes_to_str
from process_data import Stop, Route, Graph, minutes_to_str


class SearchResult(NamedTuple):
    costs: dict[Stop, float]
    came_from: dict[Stop, Optional[Route]]


def show_route_info(search_func: Callable[[Graph, Stop, Stop, int], SearchResult]):
    @wraps(search_func)
    def wrapper(graph: Graph, start: Stop, end: Stop, departure_min: int):
        start_time: float = time.time()
        result: SearchResult = search_func(graph, start, end, departure_min)
        end_time: float = time.time()

        found_path: list[Route] = get_path(result, end)
        print_path(found_path)

        sys.stderr.write(f"Czas obliczeń: {end_time - start_time:.4f}")

    return wrapper


def get_path(search_result: SearchResult, end: Stop) -> list[Route]:
    came_from: dict[Stop, Optional[Route]] = search_result.came_from
    path: list[Route] = []
    current_stop: Stop = end

    while current_stop in came_from:
        current_route = came_from[current_stop]
        if current_route is None:
            break
        path.append(current_route)
        current_stop = current_route.start_stop

    return list(reversed(path))


def print_path(path: list[Route]):
    if not path or len(path) == 0:
        print("path not found")
        return

    continous_lines: list[list[Route]] = [[]]

    for route in path:
        if len(continous_lines[-1]) == 0 or route.line == continous_lines[-1][0].line:
            continous_lines[-1].append(route)
        else:
            continous_lines.append([route])

    for line in continous_lines:
        line_summary = (
            f"{line[0].line.ljust(10)}"
            f"{line[0].start_stop.name.ljust(30)}"
            f"{minutes_to_str(line[0].departure_min).rjust(8)} -> "
            f"{line[-1].end_stop.name.ljust(30)}"
            f"{minutes_to_str(line[-1].arrival_min).rjust(8)}"
        )
        print(line_summary)
