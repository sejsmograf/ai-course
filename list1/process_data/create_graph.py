import logging
from pathlib import Path
from .graph_structure import Graph, Route, Stop
from .serialize import serialize, deserialize
from .read_csv import get_data
from .utils import minutes_from_str


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


def route_from_dict(row: dict[str, str]) -> Route:
    line = row[LINE]
    departure = row[DEPARTURE]
    arrival = row[ARRIVAL]
    start = row[START]
    end = row[END]
    start_lat = float(row[START_LAT])
    start_lon = float(row[START_LON])
    end_lat = float(row[END_LAT])
    end_lon = float(row[END_LON])

    start_stop = Stop(start, start_lat, start_lon)
    end_stop = Stop(end, end_lat, end_lon)

    return Route(
        line,
        start_stop,
        end_stop,
        minutes_from_str(departure),
        minutes_from_str(arrival),
        start_lat,
        start_lon,
        end_lat,
        end_lon,
    )


def create_graph(data: list[dict[str, str]]) -> Graph:
    graph = Graph()

    for row in data:
        graph.add_route(route_from_dict(row))

    return graph


def get_graph(serialized_path: Path = SERIALIZED_GRAPH_PATH):
    if serialized_path.exists():
        logging.info(f"Found serialized graph: {serialized_path}")
        logging.info(f"Loading serialized graph")
        graph = deserialize(serialized_path)
        return graph

    logging.warning(f"Serialized graph not found, loading data from csv")
    data: list[dict[str, str]] = get_data()

    logging.info("Data loaded, creating graph")
    graph = create_graph(data)

    logging.info(f"Serializing graph: {serialized_path}")
    serialize(graph, serialized_path)
    return graph
