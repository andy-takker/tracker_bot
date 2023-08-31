from datetime import datetime


def format_tz(tz: int) -> str:
    sign = "-" if tz < 0 else "+"
    return f"{sign}{abs(tz):02d}"


def check_time_str(time_str: str | None) -> bool:
    if time_str is None:
        return False
    try:
        parse_time_str(time_str)
    except ValueError:
        return False
    return True


def parse_time_str(time_str: str) -> datetime:
    return datetime.strptime(time_str, "%H:%M")
