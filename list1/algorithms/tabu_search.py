from .results import SearchResult, print_path, reconstruct_path
from typing import Callable
from process_data import Graph, Route, Stop
from .astar import create_astar


def create_path_between_stops(
    graph, to_visit: list[Stop], departure_min: int, search_function: Callable
) -> list[SearchResult]:
    came_from = []
    total_cost = 0
    current_min: int = departure_min

    for i in range(len(to_visit) - 1):
        start_stop: Stop = to_visit[i]
        end_stop: Stop = to_visit[i + 1]
        result: SearchResult = search_function(graph, start_stop, end_stop, current_min)
        arrival_min: int = result.came_from[end_stop].arrival_min
        came_from.append(result)
        current_min = arrival_min

    return came_from


def tabu(
    graph: Graph,
    start: Stop,
    to_visit: list[Stop],
    departure_min: int,
    search_function: Callable,
) -> SearchResult:
    results = create_path_between_stops(
        graph, [start] + to_visit + [start], departure_min, search_function
    )

    for result in results:
        path = reconstruct_path(result)
        print_path(path)
        print("\n\n")


def create_tabu(
    heuristic: Callable[[Stop, Stop], float], mode: str
) -> Callable[[Graph, Stop, list[Stop], int], SearchResult]:

    search_function: Callable = create_astar(heuristic, mode, print_result=False)

    def partially_applied_tabu_time(
        graph: Graph, start: Stop, to_visit: list[Stop], departure_min: int
    ) -> SearchResult:
        return tabu(graph, start, to_visit, departure_min, search_function)

    def partially_applied_tabu_changes(
        graph: Graph, start: Stop, to_visit: list[Stop], departure_min: int
    ) -> SearchResult:
        return tabu(graph, start, to_visit, departure_min, search_function)

    return (
        partially_applied_tabu_time if mode == "t" else partially_applied_tabu_changes
    )
