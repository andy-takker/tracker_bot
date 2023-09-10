import csv
import io
from datetime import datetime

from src.dto import TrackDTO


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


def generate_report_file(tracks: list[TrackDTO]) -> bytes:
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(TrackDTO.header())
    writer.writerows([track.to_csv_row() for track in tracks])
    return output.getvalue().encode()
