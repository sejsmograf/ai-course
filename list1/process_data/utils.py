def minutes_from_str(time_str: str) -> int:
    hours, minutes, _ = time_str.split(":")
    return int(hours) * 60 + int(minutes)


def minutes_to_str(time_minutes: int) -> str:
    hours = time_minutes // 60
    minutes = time_minutes % 60
    seconds = 0

    formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
    return formatted_time
