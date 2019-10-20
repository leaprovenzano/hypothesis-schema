import jsonschema

from hypothesis import given
from hypothesis_schema.numeric import numbers, integers


def validate_numbers(**kwargs):
    @given(numbers(**kwargs))
    def inner(data):
        assert jsonschema.validate(data, {"type": "number", **kwargs}) is None

    return inner


def validate_integers(**kwargs):
    @given(integers(**kwargs))
    def inner(data):
        assert jsonschema.validate(data, {"type": "integer", **kwargs}) is None

    return inner


test_unconstrained_integers = validate_integers()
test_minimum_integers = validate_integers(minimum=3)
test_ex_minimum_integers = validate_integers(exclusiveMinimum=3)

test_maximum_integers = validate_integers(maximum=3)
test_ex_maximum_integers = validate_integers(exclusiveMaximum=3)

test_minimum_maximum_integers = validate_integers(minimum=1, maximum=3)
test_ex_minimum_maximum_integers = validate_integers(exclusiveMinimum=1, exclusiveMaximum=5)

test_multiple_of = validate_integers(multipleOf=5)
test_multiple_with_bounds = validate_integers(minimum=1, maximum=50, multipleOf=5)


test_unconstrained_numbers = validate_numbers()
test_minimum_numbers = validate_numbers(minimum=3.5)
test_ex_minimum_numbers = validate_numbers(exclusiveMinimum=3.5)

test_maximum_numbers = validate_numbers(maximum=3.5)
test_ex_maximum_numbers = validate_numbers(exclusiveMaximum=3.5)

test_minimum_maximum_numbers = validate_numbers(minimum=1.1, maximum=3.3)
test_ex_minimum_maximum_numbers = validate_numbers(exclusiveMinimum=-1.2, exclusiveMaximum=5.88)

test_multiple_of = validate_numbers(multipleOf=5.0)
test_multiple_of_lt_one = validate_numbers(multipleOf=0.5)
test_multiple_of_lt_one_and_neg_min = validate_numbers(minimum=-1.5, multipleOf=0.5)

test_multiple_with_bounds = validate_numbers(minimum=0.1, maximum=50, multipleOf=5.0)
