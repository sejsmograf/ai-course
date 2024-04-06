from functools import partial
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

    return SearchResult(costs, came_from, visited_stops_counter)


# def astar_change(
#     graph: Graph,
#     start: Stop,
#     end: Stop,
#     departure_min: int,
#     heuristic: Callable[[Stop, Stop], float],
# ) -> SearchResult:
#     costs: dict[Stop, float] = {start: 0}
#     came_from: dict[Stop, Optional[Route]] = {start: None}
#
#
#     pq: PriorityQueue[tuple[float, Stop]] = PriorityQueue()
#     pq.put((0, start))
#
#     visited_stops_counter: int = 0
#     while not pq.empty():
#         visited_stops_counter += 1
#         _, curr_stop = pq.get()
#         curr_cost = costs[curr_stop]
#         prev_route: Optional[Route] = came_from[curr_stop]
#
#         if curr_stop == end:
#             break
#
#         for route in graph.departures[curr_stop]:
#             end_stop: Stop = route.end_stop
#             route_cost = curr_cost + (
#                 prev_route is not None and prev_route.line != route.line
#             )
#
#             if end_stop not in costs or route_cost < costs[end_stop]:
#                 costs[end_stop] = route_cost
#                 came_from[end_stop] = route
#
#                 priority = route_cost + heuristic(end_stop, end)
#                 pq.put((priority, end_stop))
#
#     return SearchResult(costs, came_from, visited_stops_counter)


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
        for route in sorted(
            graph.departures[curr_stop],
            key=lambda route: not graph.is_route_arriving(route, end),
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

    return SearchResult(costs, came_from, visited_stops_counter)


def create_astar(
    heuristic: Callable[[Stop, Stop], float], mode: str
) -> Callable[[Graph, Stop, Stop, int], SearchResult]:

    if mode == "t":
        heuristic_weight: float = 5
    elif mode == "p":
        heuristic_weight: float = 1
    else:
        raise ValueError(f"Invalid mode for creating astar: {mode}")

    @route_info_decorator
    def partially_applied_astar_time(
        graph: Graph, start: Stop, end: Stop, departure_min: int
    ) -> SearchResult:
        return astar_time(graph, start, end, departure_min, heuristic, heuristic_weight)

    @route_info_decorator
    def partially_applied_astar_change(
        graph: Graph, start: Stop, end: Stop, departure_min: int
    ) -> SearchResult:
        return astar_change(
            graph, start, end, departure_min, heuristic, heuristic_weight
        )

    return (
        partially_applied_astar_time if mode == "t" else partially_applied_astar_change
    )
