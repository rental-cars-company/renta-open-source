import re
from datetime import date

DATE_RE = re.compile(
    r"(?P<day>\d{2})\.?\s?(?P<month>\d{2})\.?\s?(?P<year>\d{4})"
)


def parse_date(text: str) -> date | None:
    match = DATE_RE.search(text)
    _date = date(
        year=int(match.group("year")),  # type: ignore
        month=int(match.group("month")),  # type: ignore
        day=int(match.group("day")),  # type: ignore
    )
    return _date
