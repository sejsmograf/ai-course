from queue import PriorityQueue
from typing import Optional
from .cost_functions import minutes_cost
from process_data import Graph, Route, Stop
from .results import SearchResult, show_route_info


@show_route_info
def dijkstra(graph: Graph, start: Stop, end: Stop, departure_min: int) -> SearchResult:
    costs: dict[Stop, float] = {start: 0}
    came_from: dict[Stop, Optional[Route]] = {start: None}

    pq: PriorityQueue[tuple[float, Stop]] = PriorityQueue()
    pq.put((0, start))

    while not pq.empty():
        curr_cost, curr_stop = pq.get()
        prev_route: Optional[Route] = came_from[curr_stop]

        if curr_stop == end:
            break

        for route in graph.stops[start]:
            end_stop: Stop = route.end_stop
            route_cost = curr_cost + minutes_cost(
                prev_route, route, int(departure_min + curr_cost)
            )

            if end_stop not in costs or route_cost < costs[end_stop]:
                costs[end_stop] = route_cost
                came_from[end_stop] = route
                pq.put((route_cost, end_stop))

    return SearchResult(costs, came_from)


#     graph: dict[str, list[Route]],
#     start_stop: str,
#     end_stop: str,
#     current_time_minutes: int,
# ):
#     start_time: float = time.time()
#     result, costs = dijkstra(graph, start_stop, end_stop, current_time_minutes)
#     end_time: float = time.time()
#
#     if end_stop in result:
#         print_path(get_path(result, end_stop))
#         sys.stderr.write(f"\n\nKoszt trasy: {costs[end_stop]}")
#     else:
#         print("\nNie znaleziono trasy")
#
#     sys.stderr.write(f"\nCzas obliczeń: {end_time - start_time:.4f}s\n")
