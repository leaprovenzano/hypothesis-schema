from typing import Union, Iterable

from hypothesis import strategies as st

Strategy = st.SearchStrategy
JSONAtomics = Union[str, int, float, bool]


booleans = st.booleans


def constants(value: JSONAtomics) -> Strategy:
    return st.just(value)


def enums(*choices: Iterable[JSONAtomics]) -> Strategy:
    return st.sampled_from(choices)
