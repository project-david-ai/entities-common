import pytest

from projectdavid_common.schemas.function_tools import validate_function_definitions


def test_nested_schema_preserved():
    definition = {
        "name": "get_flights",
        "strict": False,
        "parameters": {
            "type": "object",
            "properties": {
                "legs": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {"city": {"enum": ["London", "Paris"]}},
                        "required": ["city"],
                        "additionalProperties": False,
                    },
                }
            },
            "required": ["legs"],
            "additionalProperties": False,
        },
    }
    definitions = [definition]
    assert validate_function_definitions(definitions) is definitions


@pytest.mark.parametrize(
    "definitions",
    [
        [{}],
        [{"name": "bad name"}],
        [{"name": "web_search"}],
        [{"name": "a"}, {"name": "a"}],
        [{"name": "a", "strict": "true"}],
        [{"name": "a", "description": 1}],
        [{"name": "a", "parameters": []}],
        [
            {
                "name": "a",
                "parameters": {
                    "type": "object",
                    "properties": {"x": {"type": "bogus"}},
                },
            }
        ],
        [{"name": "a", "parameters": {"type": "object", "required": "x"}}],
        [{"name": "a", "parameters": {"type": "object", "default": float("nan")}}],
        [{"name": "a", "description": "x" * 65537}],
    ],
)
def test_invalid_definitions(definitions):
    with pytest.raises(ValueError):
        validate_function_definitions(definitions)


def test_parameterless_functions():
    definitions = [{"name": "now"}, {"name": "time", "parameters": {}}]
    assert validate_function_definitions(definitions) == definitions
