"""Validate developer-defined function declarations without rewriting schemas."""

import json
import re

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from ..constants.tools import PLATFORM_TOOLS

MAX_FUNCTIONS = 128
MAX_FUNCTION_BYTES = 65536
MAX_TOTAL_BYTES = 262144
_NAME = re.compile(r"[A-Za-z0-9_-]{1,64}")
_FIELDS = {"name", "description", "parameters", "strict"}


def validate_function_definitions(definitions: list[dict]) -> list[dict]:
    """Validate local function definitions, preserving their JSON values verbatim.

    This is a declaration check, not instance validation or provider-specific
    strict-mode validation. It never dereferences external schema references.
    Existing generic assistant tool dictionaries remain backward-compatible.
    """
    if not isinstance(definitions, list) or len(definitions) > MAX_FUNCTIONS:
        raise ValueError("Provide at most 128 function definitions.")

    seen = set()
    total = 0
    for definition in definitions:
        if not isinstance(definition, dict) or set(definition) - _FIELDS:
            raise ValueError(
                "Use a function definition with name, description, parameters and optional strict."
            )
        name = definition.get("name")
        if not isinstance(name, str) or not _NAME.fullmatch(name):
            raise ValueError(
                "Function names must contain 1–64 letters, digits, underscores or hyphens."
            )
        if name in PLATFORM_TOOLS:
            raise ValueError("A function name is reserved for platform use.")
        if name in seen:
            raise ValueError("Function names must be unique.")
        seen.add(name)
        if "description" in definition and not isinstance(
            definition["description"], str
        ):
            raise ValueError("Function description must be a string.")
        if "strict" in definition and not isinstance(definition["strict"], bool):
            raise ValueError("Function strict must be a boolean.")
        try:
            size = len(
                json.dumps(definition, ensure_ascii=False, allow_nan=False).encode(
                    "utf-8"
                )
            )
        except (TypeError, ValueError, RecursionError):
            raise ValueError(
                "Function definition must contain valid JSON values."
            ) from None
        total += size
        if size > MAX_FUNCTION_BYTES or total > MAX_TOTAL_BYTES:
            raise ValueError("Function definitions exceed the size limit.")
        if "parameters" in definition:
            schema = definition["parameters"]
            if not isinstance(schema, dict) or (
                schema and schema.get("type") != "object"
            ):
                raise ValueError("Function parameters must be an object schema.")
            try:
                Draft202012Validator.check_schema(schema)
            except (SchemaError, RecursionError, ValueError):
                raise ValueError(
                    "Function parameters contain an invalid JSON Schema."
                ) from None
    return definitions
