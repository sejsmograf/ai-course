from typing import Optional
from .results import (
    SearchResult,
    TabuSearchResult,
    tabu_route_info_decorator,
)
from typing import Callable
from process_data import Graph, Stop
from .astar import create_astar


def create_path_between_stops(
    graph, to_visit: list[Stop], departure_min: int, search_function: Callable
) -> TabuSearchResult:
    came_from: list[SearchResult] = []
    total_cost: float = 0
    current_min: int = departure_min

    for i in range(len(to_visit) - 1):
        start_stop: Stop = to_visit[i]
        end_stop: Stop = to_visit[i + 1]
        result: SearchResult = search_function(graph, start_stop, end_stop, current_min)
        arrival_min: int = result.came_from[end_stop].arrival_min
        total_cost += result.costs[end_stop]
        came_from.append(result)
        current_min = arrival_min

    return TabuSearchResult(came_from, to_visit, total_cost)


def get_neighbors(current_solution: list[Stop]) -> list[list[Stop]]:
    n = len(current_solution)
    neighbors = []

    for i in range(1, n - 1):
        for j in range(i + 1, min(i + 3, n - 1)):
            neighbor = current_solution[:]
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)

    return neighbors


def tabu_search(
    graph: Graph,
    start: Stop,
    to_visit: list[Stop],
    departure_min: int,
    search_function: Callable,
    max_iterations: int,
    tabu_list_size: Optional[int] = None,
) -> TabuSearchResult:
    best_solution: TabuSearchResult = create_path_between_stops(
        graph, [start] + to_visit + [start], departure_min, search_function
    )
    current_solution = best_solution

    tabu_list: list[TabuSearchResult] = []

    for _ in range(max_iterations):
        neighbors = get_neighbors(current_solution.to_visit)
        best_neighbor_solution = None
        best_cost = float("inf")

        for neighbor in neighbors:
            if neighbor not in tabu_list:
                neighbor_solution = create_path_between_stops(
                    graph, neighbor, departure_min, search_function
                )

                if neighbor_solution.total_cost < best_cost:
                    best_neighbor_solution = neighbor_solution
                    best_cost = neighbor_solution.total_cost

        if best_neighbor_solution is None:
            break

        current_solution = best_neighbor_solution
        tabu_list.append(best_neighbor_solution)
        if tabu_list_size and len(tabu_list) > tabu_list_size:
            tabu_list.pop(0)

        if best_neighbor_solution.total_cost < best_solution.total_cost:
            best_solution = best_neighbor_solution

    return best_solution


def create_tabu(
    heuristic: Callable[[Stop, Stop], float], mode: str
) -> Callable[[Graph, Stop, list[Stop], int], TabuSearchResult]:
    DEFAULT_MAX_ITERATIONS = 5

    search_function: Callable = create_astar(heuristic, mode, print_result=False)

    def partially_applied_tabu_time(
        graph: Graph, start: Stop, to_visit: list[Stop], departure_min: int
    ) -> TabuSearchResult:
        return tabu_search(
            graph,
            start,
            to_visit,
            departure_min,
            search_function,
            DEFAULT_MAX_ITERATIONS,
        )

    def partially_applied_tabu_changes(
        graph: Graph, start: Stop, to_visit: list[Stop], departure_min: int
    ) -> TabuSearchResult:
        return tabu_search(
            graph,
            start,
            to_visit,
            departure_min,
            search_function,
            DEFAULT_MAX_ITERATIONS,
        )

    if mode == "t":
        chosen_tabu = partially_applied_tabu_time
        function_name = "Tabu without constraints - prioritize time"
    elif mode == "p":
        chosen_tabu = partially_applied_tabu_changes
        function_name = "Tabu without constraints - prioritize time"
    else:
        raise ValueError(f"Invalid mode {mode}")

    return tabu_route_info_decorator(chosen_tabu, function_name)
