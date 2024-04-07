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
    elif prev_route.line != curr_route.line:  # there is a line change
        # modify this to take more time for change
        if curr_minutes > curr_route.departure_min:
            delay = MINUTES_IN_DAY

    return curr_route.arrival_min + delay - curr_minutes


# Distance functions should return smaller approximation than potential
# time cost of choosing the stop


def manhattan_distance(start: Stop, end: Stop) -> float:
    # usually something around 0.1 so scale it to about 1
    DISTANCE_SCALE = 10

    distance = abs(end.lat - start.lat) + abs(end.lon - start.lon)

    return distance * DISTANCE_SCALE


def haversine_distance(stop1: Stop, stop2: Stop) -> float:
    # usually around 5, so scale it down to about 1
    DISTANCE_SCALE = 1 / 5

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

    return distance_km * DISTANCE_SCALE
