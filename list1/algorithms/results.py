import sys
import time
from functools import wraps
from typing import NamedTuple, Optional, Callable
from process_data import Stop, Route, Graph


class SearchResult(NamedTuple):
    costs: dict[Stop, float]
    came_from: dict[Stop, Optional[Route]]


def show_route_info(search_func: Callable[[Graph, Stop, Stop, int], SearchResult]):
    @wraps(search_func)
    def wrapper(graph: Graph, start: Stop, end: Stop, departure_min: int):
        start_time: float = time.time()
        result: SearchResult = search_func(graph, start, end, departure_min)
        end_time: float = time.time()

        sys.stderr.write(f"Czas obliczeń: {end_time - start_time:.4f}")

    return wrapper
