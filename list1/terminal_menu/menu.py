from typing import Callable
from .helpers import prompt_dict, prompt_time
from process_data import Stop
from process_data import get_graph
from algorithms import dijkstra, create_astar, manhattan_distance, haversine_distance


def test_all_functions(graph, start, end, departure_min):
    modes = {
        "dijkstra-time": dijkstra,
        "astar-time-manhattan": create_astar(manhattan_distance, "t"),
        "astar-time-haversine": create_astar(haversine_distance, "t"),
        "astar-change-manhattan": create_astar(manhattan_distance, "p"),
        "astar-change-haversine": create_astar(haversine_distance, "p"),
    }

    for search_function in modes.values():
        search_function(graph, start, end, departure_min)


def run_menu():
    graph = get_graph()

    stops_dict: dict[str, Stop] = {str(stop): stop for stop in graph.departures}

    modes = {
        "dijkstra-time": dijkstra,
        "astar-time-manhattan": create_astar(manhattan_distance, "t"),
        "astar-time-haversine": create_astar(haversine_distance, "t"),
        "astar-change-manhattan": create_astar(manhattan_distance, "p"),
        "astar-change-haversine": create_astar(haversine_distance, "p"),
        "test-all-functions": test_all_functions,
    }

    while True:
        search_function: Callable = prompt_dict(modes, "Enter searching mode")
        start: Stop = prompt_dict(stops_dict, "Enter START stop")
        end: Stop = prompt_dict(stops_dict, "Enter END stop")
        departure_min = prompt_time("Enter departure time")

        search_function(graph, start, end, departure_min)

        input("\nPress enter to continue")
