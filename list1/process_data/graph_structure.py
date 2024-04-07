from typing import NamedTuple, Optional


class Stop(NamedTuple):
    name: str
    lat: float
    lon: float

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Stop):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"Stop: {self.name}"


class Route(NamedTuple):
    line: str
    start_stop: Stop
    end_stop: Stop
    departure_min: int
    arrival_min: int
    start_stop_lat: float
    start_stop_lon: float
    end_stop_lat: float
    end_stop_lon: float

    def __eq__(self, other) -> bool:
        if not isinstance(other, Route):
            return False
        return self.line == other.line and self.end_stop == other.end_stop

    def __hash__(self) -> int:
        return hash((self.line, self.end_stop.name))

    def __repr__(self) -> str:
        return f"{self.start_stop} -> {self.end_stop}: {self.departure_min}"


class Graph:
    def __init__(self):
        self.departures: dict[Stop, list[Route]] = {}

        self.arriving_line_names: dict[Stop, set[str]] = {}

    def add_route(self, route: Route):
        if route.start_stop not in self.departures:
            self.departures[route.start_stop] = []
            self.arriving_line_names[route.start_stop] = set()

        if route.end_stop not in self.departures:
            self.departures[route.end_stop] = []
            self.arriving_line_names[route.end_stop] = set()

        self.departures[route.start_stop].append(route)
        self.arriving_line_names[route.end_stop].add(route.line)

    def get_stop(self, name: str) -> Optional[Stop]:
        for stop in self.departures:
            if stop.name == name:
                return stop
        return None

    def is_direct_connection(self, route: Route, destination: Stop) -> bool:
        return route.line in self.arriving_line_names[destination]
