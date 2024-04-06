import math
from typing import Optional
from process_data import Stop
from process_data import Route


def minutes_cost(
    prev_route: Optional[Route], curr_route: Route, curr_minutes: int
) -> int:
    MINUTES_IN_DAY: int = 24 * 60
    delay = 0

    if prev_route is None or prev_route.line == curr_route.line:
        if curr_minutes > curr_route.departure_min:
            delay = MINUTES_IN_DAY
    elif prev_route.line != curr_route.line:  # this case if for line changes
        if curr_minutes > curr_route.departure_min:
            delay = MINUTES_IN_DAY

    return curr_route.arrival_min + delay - curr_minutes


def manhattan_distance(start: Stop, end: Stop) -> float:
    distance = abs(end.lat - start.lat) + abs(end.lon - start.lon)

    return distance


def haversine_distance(stop1: Stop, stop2: Stop) -> float:
    lat1_rad = math.radians(stop1.lat)
    lon1_rad = math.radians(stop1.lon)
    lat2_rad = math.radians(stop2.lat)
    lon2_rad = math.radians(stop2.lon)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    radius_of_earth_km = 6371.0
    distance_km = radius_of_earth_km * c

    return distance_km
