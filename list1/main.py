from typing import Callable, Optional
import argparse
import logging
import sys
from datetime import datetime

from algorithms import dijkstra, create_astar, manhattan_distance, haversine_distance
from process_data import Graph, Stop, get_graph, minutes_from_str
from terminal_menu import run_menu

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s - %(filename)s - %(message)s"
)


def valid_time(s: str):
    try:
        _ = datetime.strptime(s, "%H:%M:%S")
        return s
    except:
        raise argparse.ArgumentTypeError("Time should have format H:M:S")


if __name__ == "__main__":
    if len(sys.argv) == 1:  # run menu if no args passed
        logging.warning("No arguments passed, running terminal menu \n")
        run_menu()
        exit()

    parser = argparse.ArgumentParser()
    modes = {
        "dijkstra-time": dijkstra,
        "astar-time-manhattan": create_astar(manhattan_distance, "t"),
        "astar-time-haversine": create_astar(haversine_distance, "t"),
        "astar-change-manhattan": create_astar(manhattan_distance, "p"),
        "astar-change-haversine": create_astar(haversine_distance, "p"),
    }

    parser.add_argument("mode", choices=modes.keys(), help="Search mode")
    parser.add_argument("start_stop", type=str, help="Start stop")
    parser.add_argument("end_stop", type=str, help="End stop")
    parser.add_argument(
        "current_time",
        type=valid_time,
        help="Departur time",
    )

    args = parser.parse_args()

    selected_function: Callable = modes[args.mode]
    start_stop_name: str = args.start_stop
    end_stop_name: str = args.end_stop

    departure_time_min = minutes_from_str(args.current_time)
    graph: Graph = get_graph()

    start_stop: Optional[Stop] = graph.get_stop(start_stop_name)
    end_stop: Optional[Stop] = graph.get_stop(end_stop_name)

    if start_stop is None:
        raise ValueError("Start stop doesn't exist")
    if end_stop is None:
        raise ValueError("End stop doesn't exist")

    selected_function(graph, start_stop, end_stop, departure_time_min)
