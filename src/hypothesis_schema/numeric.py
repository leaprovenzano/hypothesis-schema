from typing import Optional

from hypothesis import strategies as st
from hypothesis_schema.utils import accept_pascalcase


Opt = Optional
Strategy = st.SearchStrategy


@accept_pascalcase
def integers(
    minimum: Opt[int] = None,
    maximum: Opt[int] = None,
    exclusive_minimum: Opt[int] = None,
    exclusive_maximum: Opt[int] = None,
    multiple_of: Opt[int] = None,
    **kwargs
) -> Strategy:
    minimum = exclusive_minimum + 1 if exclusive_minimum else minimum
    maximum = exclusive_maximum - 1 if exclusive_maximum else maximum
    strategy = st.integers(minimum, maximum)
    if multiple_of is not None:
        strategy = strategy.filter(lambda x: x % multiple_of == 0)
    return strategy


@accept_pascalcase
def numbers(
    minimum: Opt[float] = None,
    maximum: Opt[float] = None,
    exclusive_minimum: Opt[float] = None,
    exclusive_maximum: Opt[float] = None,
    multiple_of: Opt[float] = None,
    **kwargs
) -> Strategy:
    minimum = exclusive_minimum if exclusive_minimum else minimum
    maximum = exclusive_maximum if exclusive_maximum else maximum

    if multiple_of is not None:
        strategy = st.integers(minimum, maximum).map(lambda x: float(x) * multiple_of)
        if minimum is not None:
            strategy = strategy.filter(lambda x: x > minimum)
        if maximum is not None:
            strategy = strategy.filter(lambda x: x < maximum)
    else:

        strategy = st.floats(
            min_value=minimum,
            max_value=maximum,
            allow_infinity=False,
            allow_nan=False,
            exclude_max=exclusive_maximum is not None,
            exclude_min=exclusive_minimum is not None,
        )

    return strategy
