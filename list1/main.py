from process_data import Stop, Graph, minutes_from_str, get_graph
from algorithms import dijkstra
from datetime import datetime
import argparse


def valid_time(s: str):
    try:
        _ = datetime.strptime(s, "%H:%M:%S")
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
    start_stop: Stop = Stop(args.start_stop)
    end_stop: Stop = Stop(args.end_stop)
    current_time_minutes = minutes_from_str(args.current_time)
    graph: Graph = get_graph()

    if start_stop not in graph.stops:
        raise ValueError("Przystanek początkowy nie istnieje")
    if end_stop not in graph.stops:
        raise ValueError("Przystanek końcowy nie istnieje")

    dijkstra(graph, start_stop, end_stop, current_time_minutes)
