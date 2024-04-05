from queue import PriorityQueue
from typing import Optional
from .cost_functions import minutes_cost
from ..process_data import Graph, Route, Stop


def dijkstra(graph: Graph, start: Stop, end: Stop, departure_min: int):
    costs: dict[Stop, int] = {start: 0}
    came_from: dict[Stop, Optional[Route]] = {start: None}

    pq: PriorityQueue[tuple[int, Stop]] = PriorityQueue()
    pq.put((0, start))

    while not pq.empty():
        curr_cost, curr_stop = pq.get()
        prev_route: Optional[Route] = came_from[curr_stop]

        if curr_stop == end:
            return

        for route in graph.stops[start]:
            end_stop: Stop = route.end_stop
            route_cost = curr_cost + minutes_cost(
                prev_route, route, departure_min + curr_cost
            )

            if end_stop not in costs or route_cost < costs[end_stop]:
                costs[end_stop] = route_cost
                came_from[end_stop] = route
                pq.put((route_cost, end_stop))


def call_dijkstra(
    graph: dict[str, list[Route]],
    start_stop: str,
    end_stop: str,
    current_time_minutes: int,
):
    start_time: float = time.time()
    result, costs = dijkstra(graph, start_stop, end_stop, current_time_minutes)
    end_time: float = time.time()

    if end_stop in result:
        print_path(get_path(result, end_stop))
        sys.stderr.write(f"\n\nKoszt trasy: {costs[end_stop]}")
    else:
        print("\nNie znaleziono trasy")

    sys.stderr.write(f"\nCzas obliczeń: {end_time - start_time:.4f}s\n")


def valid_time(s: str):
    try:
        _ = datetime.strptime(s, TIMEFORMAT)
        return s
    except:
        raise argparse.ArgumentTypeError("Czas musi być w formacie H:M:S")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("start_stop", type=str, help="Przystanek początkowy A")
    parser.add_argument("end_stop", type=str, help="Przystanek końcowy B")
    parser.add_argument(
        "current_time",
        type=valid_time,
        help="Czas pojawienia się na przystanku początkowym",
    )

    args = parser.parse_args()
    start_stop: str = args.start_stop
    end_stop: str = args.end_stop
    current_time_minutes = minutes_from_time_str(args.current_time)
    graph: dict[str, list[Route]] = get_graph()

    if start_stop not in graph:
        raise ValueError("Przystanek początkowy nie istnieje")
    if end_stop not in graph:
        raise ValueError("Przystanek końcowy nie istnieje")

    call_dijkstra(graph, start_stop, end_stop, current_time_minutes)
