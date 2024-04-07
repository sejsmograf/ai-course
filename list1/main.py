from typing import Callable, Optional
import argparse
import logging
import sys
from datetime import datetime

from algorithms import (
    dijkstra,
    create_astar,
    manhattan_distance,
    haversine_distance,
    create_tabu,
)
from process_data import Graph, Stop, get_graph, minutes_from_str
from terminal_menu import run_menu
from log import setup_logging


def valid_time(s: str):
    try:
        _ = datetime.strptime(s, "%H:%M:%S")
        return s
    except:
        raise argparse.ArgumentTypeError("Time should have format H:M:S")


if __name__ == "__main__":
    setup_logging()

    if len(sys.argv) == 1:  # run menu if no args passed
        logging.warning("No arguments passed, running terminal menu \n")
        run_menu()
        exit()

    modes = {
        "dijkstra-time": dijkstra,
        "astar-time-manhattan": create_astar(manhattan_distance, "t"),
        "astar-time-haversine": create_astar(haversine_distance, "t"),
        "astar-changes-manhattan": create_astar(manhattan_distance, "p"),
        "astar-changes-haversine": create_astar(haversine_distance, "p"),
        "tabu-time": create_tabu(manhattan_distance, "t"),
        "tabu-changes": create_tabu(haversine_distance, "p"),
    }

    parser = argparse.ArgumentParser()

    parser.add_argument("mode", choices=modes.keys(), help="Search mode")
    parser.add_argument("start_stop", type=str, help="Start stop")
    parser.add_argument("end_stop", type=str, help="End stop")
    parser.add_argument(
        "current_time",
        type=valid_time,
        help="Departur time",
    )

    args = parser.parse_args()

    selected_mode: Callable = modes[args.mode]
    start_stop_name: str = args.start_stop
    end_stop_name: str = args.end_stop
    departure_time_min = minutes_from_str(args.current_time)

    graph: Graph = get_graph()
    start_stop: Optional[Stop] = graph.get_stop(start_stop_name)

    if start_stop is None:
        raise ValueError(f"Start stop: {start_stop} doesn't exist")

    if args.mode == "tabu-time" or args.mode == "tabu-changes":
        to_visit_names: list[str] = args.end_stop.split(";")
        to_visit: list[Stop] = []

        for stop_name in to_visit_names:
            existing_stop: Optional[Stop] = graph.get_stop(stop_name)
            if existing_stop is None:
                raise ValueError(f"Stop {stop_name} doesn't exist")
            to_visit.append(existing_stop)
        selected_mode(graph, start_stop, to_visit, departure_time_min)
        exit(0)

    end_stop: Optional[Stop] = graph.get_stop(end_stop_name)

    if end_stop is None:
        raise ValueError("End stop doesn't exist")

    selected_mode(graph, start_stop, end_stop, departure_time_min)
