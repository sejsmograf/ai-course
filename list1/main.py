import logging
import sys
from terminal_menu import run_menu
from process_data import Stop, Graph, minutes_from_str, get_graph
from algorithms import dijkstra
from datetime import datetime
import argparse

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

    parser.add_argument("mode", choices=["dijkstra-time"], help="Search mode")
    parser.add_argument("start_stop", type=str, help="Start stop")
    parser.add_argument("end_stop", type=str, help="End stop")
    parser.add_argument(
        "current_time",
        type=valid_time,
        help="Departure time",
    )

    args = parser.parse_args()

    start_stop: Stop = Stop(args.start_stop)
    end_stop: Stop = Stop(args.end_stop)
    current_time_minutes = minutes_from_str(args.current_time)
    graph: Graph = get_graph()

    if start_stop not in graph.stops:
        raise ValueError("Start stop doesn't exist")
    if end_stop not in graph.stops:
        raise ValueError("End stop doesn't exist")

    dijkstra(graph, start_stop, end_stop, current_time_minutes)
