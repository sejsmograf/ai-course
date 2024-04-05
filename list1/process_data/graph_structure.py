from typing import NamedTuple


class Stop(NamedTuple):
    name: str


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


class Graph:
    def __init__(self):
        self.stops: dict[Stop, list[Route]] = {}

    def add_route(self, route: Route):
        if route.start_stop not in self.stops:
            self.stops[route.start_stop] = []

        if route.end_stop not in self.stops:
            self.stops[route.end_stop] = []

        self.stops[route.start_stop].append(route)
