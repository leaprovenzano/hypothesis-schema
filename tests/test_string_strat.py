from typing import Callable
import string

import jsonschema

from hypothesis import given
from hypothesis_schema.strings import schema_strings


def validate_data_from_schema(test: Callable = None, **kwargs):
    @given(schema_strings(**kwargs))
    def inner(data):
        assert jsonschema.validate(data, {"type": "string", **kwargs}) is None
        if test is not None:
            test(data)

    return inner


def contains_kwd(s: str):
    assert "boop" in s


def all_alphalower(s: str):
    assert all(c in string.ascii_lowercase for c in s)


test_uuid_format_string = validate_data_from_schema(format="uuid")
test_email_format_string = validate_data_from_schema(format="email")
test_idn_email_format_string = validate_data_from_schema(format="idn-email")
test_date_time_format_string = validate_data_from_schema(format="date-time")
test_date_format_string = validate_data_from_schema(format="date")
test_time_format_string = validate_data_from_schema(format="time")
test_ipv4_format_string = validate_data_from_schema(format="ipv4")
test_ipv6_format_string = validate_data_from_schema(format="ipv6")

test_pattern_with_min_and_max_length = validate_data_from_schema(pattern=r"^[a-z]+$", minLength=1, maxLength=10)
test_pattern_with_min_length = validate_data_from_schema(pattern=r"^[a-z]*$", minLength=5)
test_pattern_with_max_length = validate_data_from_schema(pattern=r"^[a-z]*$", maxLength=5)
test_pattern_with_fullmatch = validate_data_from_schema(test=all_alphalower, pattern=r"^[a-z]+$")
test_pattern_without_fullmatch = validate_data_from_schema(test=contains_kwd, pattern=r"boop")


test_standard_string = validate_data_from_schema()
test_string_with_min_length = validate_data_from_schema(minLength=6)
test_string_with_max_length = validate_data_from_schema(maxLength=6)
test_string_with_min_and_max_length = validate_data_from_schema(minLength=3, maxLength=6)
