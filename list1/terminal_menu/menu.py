from typing import Callable
from algorithms import create_tabu
from .helpers import prompt_dict, prompt_many_dict, prompt_time
from process_data import Stop, Graph
from process_data import get_graph
from algorithms import dijkstra, create_astar, manhattan_distance, haversine_distance


def test_all_functions(graph, start, end, departure_min):
    modes = {
        "dijkstra-time": dijkstra,
        "astar-time-manhattan": create_astar(manhattan_distance, "t"),
        "astar-time-haversine": create_astar(haversine_distance, "t"),
        "astar-changes-manhattan": create_astar(manhattan_distance, "p"),
        "astar-changes-haversine": create_astar(haversine_distance, "p"),
    }

    for search_function in modes.values():
        search_function(graph, start, end, departure_min)


def run_search_menu(graph: Graph):
    stops_dict: dict[str, Stop] = {str(stop): stop for stop in graph.departures}
    modes = {
        "dijkstra-time": dijkstra,
        "astar-time-manhattan": create_astar(manhattan_distance, "t"),
        "astar-time-haversine": create_astar(haversine_distance, "t"),
        "astar-changes-manhattan": create_astar(manhattan_distance, "p"),
        "astar-changes-haversine": create_astar(haversine_distance, "p"),
        "test-all-functions": test_all_functions,
    }

    while True:
        search_function: Callable = prompt_dict(modes, "Enter searching mode")
        start: Stop = prompt_dict(stops_dict, "Enter START stop")
        end: Stop = prompt_dict(stops_dict, "Enter END stop")
        departure_min = prompt_time("Enter departure time")

        search_function(graph, start, end, departure_min)

        input("\nPress enter to continue")


def run_tabu_menu(graph: Graph):
    stops_dict: dict[str, Stop] = {str(stop): stop for stop in graph.departures}
    modes = {
        "tabu-time": create_tabu(haversine_distance, "t"),
        "tabu-changes": create_tabu(haversine_distance, "p"),
    }

    search_function: Callable = prompt_dict(modes, "Enter searching mode")
    start: Stop = prompt_dict(stops_dict, "Enter START stop")
    to_visit: list[Stop] = prompt_many_dict(stops_dict, "Enter stops to visit")
    departure_min = prompt_time("Enter departure time")

    search_function(graph, start, to_visit, departure_min)


def run_menu():
    graph = get_graph()

    tasks = {"From A to B": 0, "Between list of stops": 1}

    task = prompt_dict(tasks, "Select task")

    if task == 0:
        run_search_menu(graph)
    elif task == 1:
        run_tabu_menu(graph)
