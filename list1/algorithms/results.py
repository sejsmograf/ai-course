import logging
from functools import wraps
import sys
import time
from typing import NamedTuple, Optional, Callable
from process_data.utils import minutes_to_str
from process_data import Stop, Route, Graph, minutes_to_str


class TabuSearchResult(NamedTuple):
    results: list["SearchResult"]
    to_visit: list[Stop]
    total_cost: float

    def __eq__(self, other):
        if not isinstance(other, TabuSearchResult):
            return False
        return self.to_visit == other.to_visit


class SearchResult(NamedTuple):
    costs: dict[Stop, float]
    came_from: dict[Stop, Optional[Route]]
    end_stop: Stop
    visited_stops: int


def route_info_decorator(
    search_func: Callable[[Graph, Stop, Stop, int], SearchResult],
    func_name: Optional[str] = None,
):
    if func_name is None:
        func_name = search_func.__name__

    @wraps(search_func)
    def wrapper(graph: Graph, start: Stop, end: Stop, departure_min: int):
        print("\n")
        logging.info(f"Running {func_name}, from {start.name} to {end.name}\n")

        start_time: float = time.time()
        result: SearchResult = search_func(graph, start, end, departure_min)
        end_time: float = time.time()

        try:
            found_path: list[Route] = reconstruct_path(result)
        except Exception as e:
            logging.error(e)
            return

        print_path(found_path)

        sys.stderr.write(f"\nCost function value: {result.costs[end]}")
        sys.stderr.write(f"\nVisited {result.visited_stops} stops before finishing")
        sys.stderr.write(f"\nSearch time: {end_time - start_time:.4f}s\n")

        return result

    return wrapper


def tabu_route_info_decorator(
    search_func: Callable[[Graph, Stop, list[Stop], int], TabuSearchResult],
    func_name: Optional[str] = None,
):
    if func_name is None:
        func_name = search_func.__name__

    @wraps(search_func)
    def wrapper(graph: Graph, start: Stop, to_visit: list[Stop], departure_min: int):
        print("\n")
        logging.info(
            f"Running {func_name}, from {start.name} between {[stop.name for stop in to_visit]}\n"
        )

        start_time: float = time.time()
        try:
            result: TabuSearchResult = search_func(
                graph, start, to_visit, departure_min
            )
        except Exception as e:
            logging.error(e)
            logging.error("Possible cause: couldn't find a way to one or many stops")
            return
        end_time: float = time.time()

        print("Found solution is to visit the stops in order:")
        print((" -> ").join([stop.name for stop in result.to_visit]))

        try:
            for i in range(len(result.results)):
                print(f"Path to {result.to_visit[i+1].name}")
                found_path: list[Route] = reconstruct_path(result.results[i])
                print_path(found_path)
                print()

        except error as e:
            logging.error(e)
            return

        sys.stderr.write(f"\nCost function value: {result.total_cost}")
        sys.stderr.write(f"\nSearch time: {end_time - start_time:.4f}s\n")

        return result

    return wrapper


def reconstruct_path(search_result: SearchResult) -> list[Route]:
    end: Stop = search_result.end_stop
    came_from: dict[Stop, Optional[Route]] = search_result.came_from

    if end not in came_from:
        raise Exception("Path not found")

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
