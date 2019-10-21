from types import MappingProxyType
from typing import Optional, Callable, Dict, Any, List

from hypothesis import strategies as st
from hypothesis_schema.utils import accept_pascalcase
from hypothesis_schema.strings import strings
from hypothesis_schema.numeric import numbers, integers
from hypothesis_schema.simple import booleans, constants, enums, nulls


Opt = Optional
Strategy = st.SearchStrategy


def is_strategy(x) -> bool:
    assert isinstance(x, Strategy)


def is_ref(x: Dict[str, Any]) -> bool:
    return list(x) == ["$ref"]


class SchemaBuilder:

    _type_dispatch = MappingProxyType(
        {"string": strings, "number": numbers, "integer": integers, "boolean": booleans, "null": nulls}
    )

    def __init__(self, schema):
        self._schema = schema.copy()
        self._definitions = self._schema.pop("definitions", None)

    def type_dispatch(self, typestr: str, **kwargs) -> Callable:
        try:
            return self._type_dispatch[typestr](**kwargs)
        except KeyError:
            if typestr == "object":
                return self.object_schema(**kwargs)
            elif typestr == "array":
                return self.array_schema(**kwargs)
        raise ValueError(f"dispatch not found for type {typestr} not found.")

    def get_ref(self, ref: str) -> Strategy:
        k = ref.lstrip("#/definitions/")  # noqa: B005

        reffed = self._definitions[k]
        if is_strategy(reffed):
            return reffed
        return self.dispatch(**reffed)

    def _get_object_properies(self, properties, required: List[str] = None, **kwargs):
        # TODO : add patten properties
        fields = {}
        for k, v in properties.items():
            if is_ref(v):
                strat = self.get_ref(v["$ref"])
            else:
                strat = self.dispatch(**v)

            fields[k] = strat
        if required is not None:
            if len(set(required) - set(fields)) > 1:
                optional = {k: v for k, v in fields.items() if k not in required}
            else:
                optional = None
        else:
            optional = fields
            fields = {}
        strategy = st.fixed_dictionaries(fields, optional=optional)
        return strategy

    def object_schema(self, properties, required: List[str] = None, **kwargs):
        # TODO : add patten properties
        # TODO : add additional properties
        # TODO : add dependencies
        # TODO : return random stuff when no properties are specified
        strat = self._get_object_properies(properties=properties, required=required, **kwargs)
        return strat

    @accept_pascalcase
    def _list_items(
        self, items, min_items: int = 0, max_items: Optional[int] = None, unique_items: bool = False, **kwargs
    ):
        if is_ref(items):
            elements = self.get_ref(items["$ref"])
        else:
            elements = self.dispatch(**items)
        return st.lists(elements, min_size=min_items, max_size=max_items, unique=unique_items)

    # TODO: Write me
    def _tuple_items(self, items, **kwargs):
        raise NotImplementedError("support for tuple items is not currently supported")

    def array_schema(self, items, **kwargs):
        if isinstance(items, dict):
            return self._list_items(items, **kwargs)

    def dispatch(self, type: str = None, enum=None, constant=None, **kwargs):
        if enum is not None:
            return enums(*enum)
        if constant is not None:
            return constants(constant)
        return self.type_dispatch(type, **kwargs)

    def _build_definitions(self):
        if self._definitions is not None:
            for k, v in self._definitions.items():
                self._definitions[k] = self.dispatch(**v)

    def build(self):
        self._build_definitions()
        return self.dispatch(**self._schema)
