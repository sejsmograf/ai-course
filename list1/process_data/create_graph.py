from pathlib import Path
from .graph_structure import Graph, Route, Stop
from .serialize import serialize, deserialize
from .read_csv import get_data

SERIALIZED_GRAPH_PATH = (
    Path(__file__).resolve().parent.parent / "data/serialized_graph.pickle"
)

LINE = "line"
DEPARTURE = "departure_time"
ARRIVAL = "arrival_time"
START = "start_stop"
END = "end_stop"
START_LAT = "start_stop_lat"
START_LON = "start_stop_lon"
END_LAT = "end_stop_lat"
END_LON = "end_stop_lon"


def minutes_from_str(time_str: str) -> int:
    hours, minutes, _ = time_str.split(":")
    return int(hours) * 60 + int(minutes)


def route_from_dict(row: dict[str, str]) -> Route:
    line = row[LINE]
    departure = row[DEPARTURE]
    arrival = row[ARRIVAL]
    start = row[START]
    end = row[END]
    start_lat = row[START_LAT]
    start_lon = row[START_LON]
    end_lat = row[END_LAT]
    end_lon = row[END_LON]

    start_stop = Stop(start)
    end_stop = Stop(end)

    return Route(
        line,
        start_stop,
        end_stop,
        minutes_from_str(departure),
        minutes_from_str(arrival),
        float(start_lat),
        float(start_lon),
        float(end_lat),
        float(end_lon),
    )


def create_graph(data: list[dict[str, str]]) -> Graph:
    graph = Graph()

    for row in data:
        graph.add_route(route_from_dict(row))

    return graph


def get_graph(serialized_path: Path = SERIALIZED_GRAPH_PATH):
    if serialized_path.exists():
        graph = deserialize(serialized_path)
        return graph

    data: list[dict[str, str]] = get_data()
    graph = create_graph(data)

    serialize(graph, serialized_path)
    return graph
