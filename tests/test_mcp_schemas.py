import pytest
from pydantic import ValidationError

from projectdavid_common.schemas.mcp_schemas import (
    AssistantMcpToolsAttach,
    McpServerRegistrationCreate,
    McpServerRegistrationUpdate,
)


def test_registration_contract_is_streamable_http_only():
    registration = McpServerRegistrationCreate(
        name=" GitHub ",
        url="https://example.test/mcp",
    )

    assert registration.name == "GitHub"
    assert registration.transport == "streamable_http"
    assert registration.timeout_seconds == 30.0


def test_registration_contract_rejects_credentials():
    with pytest.raises(ValidationError):
        McpServerRegistrationCreate(
            name="GitHub",
            url="https://example.test/mcp",
            authorization="Bearer secret",
        )


def test_registration_contract_rejects_non_http_transport():
    with pytest.raises(ValidationError):
        McpServerRegistrationCreate(
            name="Local",
            url="https://example.test/mcp",
            transport="stdio",
        )


def test_attachment_contract_rejects_duplicate_remote_names():
    with pytest.raises(ValidationError):
        AssistantMcpToolsAttach(
            server_id="mcpreg_123",
            tools=["search.issues", "search.issues"],
        )


def test_registration_update_is_explicit_and_mutable_only():
    update = McpServerRegistrationUpdate(
        name="GitHub Production",
        timeout_seconds=45,
        enabled=False,
    )

    assert update.name == "GitHub Production"
    assert update.timeout_seconds == 45
    assert update.enabled is False
