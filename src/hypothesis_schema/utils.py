from typing import Callable
import re
from functools import lru_cache

_pascal_exp = re.compile(r"([a-z\d])([A-Z])")


@lru_cache(128)
def to_snakecase(s: str) -> str:
    return _pascal_exp.sub(r"\1_\2", s).lower()


def accept_pascalcase(f: Callable):
    """decorator for converting keyword args from pascalcase to snake case.
    """

    def inner(*args, **kwargs):
        return f(*args, **{to_snakecase(k): v for k, v in kwargs.items()})

    return inner
