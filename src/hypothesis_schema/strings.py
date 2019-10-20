from typing import Optional

from hypothesis import strategies as st
from hypothesis import provisional as pst
from hypothesis_schema.utils import accept_pascalcase

Strategy = st.SearchStrategy


class InvalidFormatError(ValueError):

    def __init__(self, fmt: str):
        super().__init__(f"{fmt} is not currently supported.")


FORMATS = {
    "uuid": st.uuids().map(str),
    "email": st.emails(),
    "idn-email": st.emails(),
    "date-time": st.datetimes().map(lambda x: x.isoformat()),
    "date": st.dates().map(lambda x: x.isoformat()),
    "time": st.times().map(lambda x: x.isoformat()),
    "ipv4": pst.ip4_addr_strings(),
    "ipv6": pst.ip6_addr_strings(),
}


def format_strings(fmt: str) -> Strategy:
    try:
        return FORMATS[fmt]
    except KeyError:
        raise InvalidFormatError(fmt)


def pattern_strings(pattern: str, min_length: Optional[int] = None, max_length: Optional[int] = None) -> Strategy:
    if pattern[-1] == "$":
        pattern = rf"{pattern[:-1]}\Z"
    schema = st.from_regex(pattern)
    if min_length is not None:
        schema = schema.filter(lambda x: len(x) >= min_length)
    if max_length is not None:
        schema = schema.filter(lambda x: len(x) <= max_length)
    return schema


@accept_pascalcase
def schema_strings(
    min_length: int = 0, max_length: Optional[int] = None, pattern: Optional[str] = None, format: Optional[str] = None
) -> Strategy:
    if format is not None:
        return format_strings(format)
    elif pattern is not None:
        return pattern_strings(pattern, min_length=min_length, max_length=max_length)
    return st.text(min_size=min_length, max_size=max_length)
