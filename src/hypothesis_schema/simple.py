from typing import Union, Iterable

from hypothesis import strategies as st

Strategy = st.SearchStrategy
JSONAtomics = Union[str, int, float, bool]


def booleans(**kwargs):
    return st.booleans()


def nulls(**kwargs):
    return st.none()


def constants(value: JSONAtomics, **kwargs) -> Strategy:
    return st.just(value)


def enums(*choices: Iterable[JSONAtomics], **kwargs) -> Strategy:
    return st.sampled_from(choices)
