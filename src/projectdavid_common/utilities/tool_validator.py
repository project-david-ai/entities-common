# src/projectdavid_common/utilities/tool_validator.py
import logging
from typing import Any, Dict, List, Optional

# LOG = logging.getLogger(__name__)


class ToolValidator:
    """SDK-side validation to ensure LLM tool calls match Assistant schemas."""

    def __init__(self):
        self.schema_registry: Dict[str, List[str]] = {}

    def build_registry_from_assistant(self, tools: List[Dict[str, Any]]):
        """Parses Assistant tool definitions to map required fields."""
        registry = {}
        for tool_entry in tools:
            if tool_entry.get("type") == "function":
                func = tool_entry.get("function", {})
                name = func.get("name")
                params = func.get("parameters", {})
                required = params.get("required", [])
                if name:
                    registry[name] = required
        self.schema_registry = registry

        # Standard logging usage
        # LOG.info(f"[Validator] Registry built for {len(self.schema_registry)} tools.")

    def validate_args(self, tool_name: str, args: Dict[str, Any]) -> Optional[str]:
        """Returns error string if required fields are missing, else None."""
        required = self.schema_registry.get(tool_name, [])

        # Handle cases where args might be None
        safe_args = args if args else {}

        missing = [f for f in required if f not in safe_args or safe_args[f] in [None, ""]]

        if missing:
            error_msg = f"Validation Error: The tool '{tool_name}' requires missing arguments: {', '.join(missing)}."
            # LOG.warning(f"[Validator] {error_msg}")
            return error_msg

        return None
