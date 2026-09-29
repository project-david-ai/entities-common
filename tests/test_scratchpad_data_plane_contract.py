from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from projectdavid_common import ValidationInterface


def test_scratchpad_data_plane_contracts_are_exported() -> None:
    names = [
        "ScratchpadContentUpdate",
        "ScratchpadContentRead",
        "ScratchpadEntryCreate",
        "ScratchpadEntryRead",
        "ScratchpadEntryList",
        "ScratchpadStateCleared",
    ]

    for name in names:
        assert (
            getattr(
                ValidationInterface,
                name,
                None,
            )
            is not None
        )


def test_content_update_accepts_empty_body_but_forbids_extra_fields() -> None:
    payload = ValidationInterface.ScratchpadContentUpdate(
        content="",
    )

    assert payload.content == ""

    with pytest.raises(ValidationError):
        ValidationInterface.ScratchpadContentUpdate(
            content="plan",
            owner_id="user_forbidden",
        )


def test_content_read_models_unmaterialized_and_materialized_state() -> None:
    empty = ValidationInterface.ScratchpadContentRead(
        scratchpad_id="scratchpad_1",
        content="",
        updated_at=None,
    )

    assert empty.updated_at is None

    now = datetime.now(timezone.utc)

    populated = ValidationInterface.ScratchpadContentRead(
        scratchpad_id="scratchpad_1",
        content="working plan",
        updated_at=now,
    )

    assert populated.content == "working plan"
    assert populated.updated_at == now


def test_entry_create_requires_non_empty_content() -> None:
    entry = ValidationInterface.ScratchpadEntryCreate(
        content="verified finding",
    )

    assert entry.content == "verified finding"

    with pytest.raises(ValidationError):
        ValidationInterface.ScratchpadEntryCreate(
            content="",
        )


def test_entry_list_preserves_order() -> None:
    first_time = datetime(
        2026,
        9,
        29,
        12,
        0,
        tzinfo=timezone.utc,
    )

    second_time = datetime(
        2026,
        9,
        29,
        12,
        1,
        tzinfo=timezone.utc,
    )

    listing = ValidationInterface.ScratchpadEntryList(
        data=[
            ValidationInterface.ScratchpadEntryRead(
                scratchpad_id="scratchpad_1",
                content="worker-a",
                created_at=first_time,
            ),
            ValidationInterface.ScratchpadEntryRead(
                scratchpad_id="scratchpad_1",
                content="worker-b",
                created_at=second_time,
            ),
        ]
    )

    assert listing.object == "list"
    assert [entry.content for entry in listing.data] == [
        "worker-a",
        "worker-b",
    ]


@pytest.mark.parametrize(
    "scope",
    [
        "content",
        "entries",
        "all",
    ],
)
def test_state_cleared_supports_only_defined_scopes(
    scope: str,
) -> None:
    result = ValidationInterface.ScratchpadStateCleared(
        id="scratchpad_1",
        scope=scope,
    )

    assert result.id == "scratchpad_1"
    assert result.object == "scratchpad.state.cleared"
    assert result.scope == scope
    assert result.cleared is True


def test_state_cleared_rejects_unknown_scope() -> None:
    with pytest.raises(ValidationError):
        ValidationInterface.ScratchpadStateCleared(
            id="scratchpad_1",
            scope="everything",
        )
