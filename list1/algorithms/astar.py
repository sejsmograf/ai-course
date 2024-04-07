from queue import PriorityQueue
from .results import SearchResult, route_info_decorator
from typing import Callable, Optional
from .cost_functions import minutes_cost
from process_data import Graph, Route, Stop


def astar_time(
    graph: Graph,
    start: Stop,
    end: Stop,
    departure_min: int,
    heuristic: Callable[[Stop, Stop], float],
    heuristic_weight: float,
) -> SearchResult:
    costs: dict[Stop, float] = {start: 0}
    came_from: dict[Stop, Optional[Route]] = {start: None}

    pq: PriorityQueue[tuple[float, Stop]] = PriorityQueue()
    pq.put((0, start))

    visited_stops_counter: int = 0
    while not pq.empty():
        visited_stops_counter += 1
        _, curr_stop = pq.get()
        curr_cost = costs[curr_stop]
        prev_route: Optional[Route] = came_from[curr_stop]

        if curr_stop == end:
            break

        for route in graph.departures[curr_stop]:
            end_stop: Stop = route.end_stop
            route_cost = curr_cost + minutes_cost(
                prev_route, route, int(departure_min + curr_cost)
            )

            if end_stop not in costs or route_cost < costs[end_stop]:
                costs[end_stop] = route_cost
                came_from[end_stop] = route

                priority = route_cost + heuristic(end_stop, end) * heuristic_weight
                pq.put((priority, end_stop))

    return SearchResult(costs, came_from, end, visited_stops_counter)


def astar_change_naive(
    graph: Graph,
    start: Stop,
    end: Stop,
    departure_min: int,
    heuristic: Callable[[Stop, Stop], float],
    heuristic_weight: float,
) -> SearchResult:
    costs: dict[Stop, float] = {start: 0}
    came_from: dict[Stop, Optional[Route]] = {start: None}

    pq: PriorityQueue[tuple[float, Stop]] = PriorityQueue()
    pq.put((0, start))

    visited_stops_counter: int = 0
    while not pq.empty():
        visited_stops_counter += 1
        _, curr_stop = pq.get()
        curr_cost = costs[curr_stop]
        prev_route: Optional[Route] = came_from[curr_stop]

        if curr_stop == end:
            break

        for route in graph.departures[curr_stop]:
            end_stop: Stop = route.end_stop
            route_cost = curr_cost + (
                prev_route is not None and prev_route.line != route.line
            )

            if end_stop not in costs or route_cost < costs[end_stop]:
                costs[end_stop] = route_cost
                came_from[end_stop] = route

                priority = route_cost + heuristic(end_stop, end) * heuristic_weight
                pq.put((priority, end_stop))

    return SearchResult(costs, came_from, end, visited_stops_counter)


def astar_change(
    graph: Graph,
    start: Stop,
    end: Stop,
    departure_min: int,
    heuristic: Callable[[Stop, Stop], float],
    heuristic_weight: float,
) -> SearchResult:

    costs: dict[Stop, float] = {start: 0}
    came_from: dict[Stop, Optional[Route]] = {start: None}

    pq: PriorityQueue[tuple[float, Stop]] = PriorityQueue()
    pq.put((0, start))

    visited_stops_counter: int = 0
    while not pq.empty():
        visited_stops_counter += 1
        _, curr_stop = pq.get()
        curr_cost = costs[curr_stop]
        prev_route: Optional[Route] = came_from[curr_stop]

        if curr_stop == end:
            break

        # sort all departing routes in order to check the ones directly connected with end stop first
        # also take into account the arrival time
        def sort_key(route: Route) -> int:
            # Priorityize direct connetion over minutes
            DIRECT_CONNECTION_WEIGHT = 10000

            minutes_to_arrive: int = minutes_cost(
                prev_route,
                route,
                (prev_route.arrival_min if prev_route is not None else departure_min),
            )
            no_direct_connection: bool = not graph.is_direct_connection(route, end)

            if minutes_to_arrive < 0:
                print(minutes_to_arrive)

            return no_direct_connection * DIRECT_CONNECTION_WEIGHT + minutes_to_arrive

        for route in sorted(
            graph.departures[curr_stop], key=lambda route: sort_key(route)
        ):
            end_stop: Stop = route.end_stop
            route_cost = curr_cost + (
                prev_route is not None and prev_route.line != route.line
            )

            if end_stop not in costs or route_cost < costs[end_stop]:
                costs[end_stop] = route_cost
                came_from[end_stop] = route

                priority = route_cost + heuristic(end_stop, end) * heuristic_weight
                pq.put((priority, end_stop))

    return SearchResult(costs, came_from, end, visited_stops_counter)


def create_astar(
    heuristic: Callable[[Stop, Stop], float], mode: str, print_result: bool = True
) -> Callable[[Graph, Stop, Stop, int], SearchResult]:

    if mode == "t":
        heuristic_weight: float = 20
    elif mode == "p" or mode == "p-naive":
        heuristic_weight: float = 0.5

    else:
        raise ValueError(f"Invalid mode for creating astar: {mode}")

    def partially_applied_astar_time(
        graph: Graph, start: Stop, end: Stop, departure_min: int
    ) -> SearchResult:
        return astar_time(graph, start, end, departure_min, heuristic, heuristic_weight)

    def partially_applied_astar_change(
        graph: Graph, start: Stop, end: Stop, departure_min: int
    ) -> SearchResult:
        return astar_change(
            graph, start, end, departure_min, heuristic, heuristic_weight
        )

    def partially_applied_astar_change_naive(
        graph: Graph, start: Stop, end: Stop, departure_min: int
    ) -> SearchResult:
        return astar_change_naive(
            graph, start, end, departure_min, heuristic, heuristic_weight
        )

    astar = None
    function_name: str

    if mode == "t":
        astar = partially_applied_astar_time
        function_name = "Astar - prioritize time"
    elif mode == "p":
        astar = partially_applied_astar_change
        function_name = "Astar - prioritize changes improved"
    elif mode == "p-naive":
        astar = partially_applied_astar_change_naive
        function_name = "Astar - prioritize changes naive"

    return route_info_decorator(astar, function_name) if print_result else astar
