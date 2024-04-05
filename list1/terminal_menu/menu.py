from collections.abc import Callable
from .helpers import prompt_dict, prompt_time
from process_data import Stop
from process_data import get_graph
from algorithms import dijkstra


def run_menu():
    graph = get_graph()

    stops_dict: dict[str, Stop] = {str(stop): stop for stop in graph.stops}
    search_functions: dict[str, Callable] = {"Dijkstra": dijkstra}

    while True:
        search_function: Callable = prompt_dict(
            search_functions, "Enter searching mode"
        )
        start: Stop = prompt_dict(stops_dict, "Enter START stop")
        end: Stop = prompt_dict(stops_dict, "Enter END stop")
        departure_min = prompt_time("Enter departure time")

        search_function(graph, start, end, departure_min)

        input("\nPress enter to continue")
