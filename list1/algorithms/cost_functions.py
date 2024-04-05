from typing import Optional
from ..process_data import Route


def minutes_cost(
    prev_route: Optional[Route], curr_route: Route, curr_minutes: int
) -> int:
    MINUTES_IN_DAY: int = 24 * 60
    delay = 0

    if prev_route is None or prev_route.line == curr_route.line:
        if curr_minutes <= curr_route.departure_min:
            delay = MINUTES_IN_DAY
    elif prev_route.line != curr_route.line:  # this case if for line changes
        if curr_minutes <= curr_route.departure_min:
            delay = MINUTES_IN_DAY

    return curr_route.arrival_min + delay - curr_minutes
