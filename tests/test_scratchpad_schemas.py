from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from projectdavid_common import ValidationInterface
from projectdavid_common.schemas.scratchpads_schema import (
    ScratchpadCreate,
    ScratchpadDeleted,
    ScratchpadList,
    ScratchpadRead,
    ScratchpadUpdate,
)
from projectdavid_common.utilities.identifier_service import IdentifierService


def test_scratchpad_create_accepts_thread_id_only():
    payload = ScratchpadCreate(thread_id="thread_test")

    assert payload.thread_id == "thread_test"

    with pytest.raises(ValidationError):
        ScratchpadCreate(
            thread_id="thread_test",
            owner_id="user_must_not_be_client_supplied",
        )


def test_scratchpad_read_contract():
    now = datetime.now(timezone.utc)

    scratchpad = ScratchpadRead(
        id="scratchpad_test",
        owner_id="user_test",
        thread_id="thread_test",
        created_at=now,
        updated_at=now,
        meta_data={},
    )

    assert scratchpad.id == "scratchpad_test"
    assert scratchpad.owner_id == "user_test"
    assert scratchpad.thread_id == "thread_test"


def test_scratchpad_update_is_metadata_only():
    update = ScratchpadUpdate(meta_data={"purpose": "research"})

    assert update.meta_data == {"purpose": "research"}

    with pytest.raises(ValidationError):
        ScratchpadUpdate(content="must-live-in-redis")


def test_scratchpad_list_and_delete_contracts():
    now = datetime.now(timezone.utc)

    scratchpad = ScratchpadRead(
        id="scratchpad_test",
        owner_id="user_test",
        thread_id="thread_test",
        created_at=now,
        updated_at=now,
        meta_data={},
    )

    listing = ScratchpadList(data=[scratchpad])
    deleted = ScratchpadDeleted(id=scratchpad.id)

    assert listing.object == "list"
    assert listing.data == [scratchpad]
    assert deleted.object == "scratchpad.deleted"
    assert deleted.deleted is True


def test_validation_interface_exposes_scratchpad_contracts():
    assert ValidationInterface.ScratchpadCreate is ScratchpadCreate
    assert ValidationInterface.ScratchpadRead is ScratchpadRead
    assert ValidationInterface.ScratchpadUpdate is ScratchpadUpdate
    assert ValidationInterface.ScratchpadList is ScratchpadList
    assert ValidationInterface.ScratchpadDeleted is ScratchpadDeleted


def test_identifier_service_generates_scratchpad_id():
    scratchpad_id = IdentifierService.generate_scratchpad_id()

    assert isinstance(scratchpad_id, str)
    assert scratchpad_id
