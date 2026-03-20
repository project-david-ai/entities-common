# src/projectdavid_common/schemas/device_ingest_schema.py

from typing import List, Optional

from pydantic import BaseModel, Field, validator


class DeviceIngest(BaseModel):
    """
    Represents a single network device to be ingested into the inventory.

    `host_name` is the primary key within a user's inventory partition.
    `platform` must be a Netmiko-compatible device type string
    (e.g. 'cisco_ios', 'arista_eos', 'juniper_junos').
    """

    host_name: str
    ip_address: Optional[str] = None
    platform: str = Field(..., description="Netmiko-compatible device type, e.g. cisco_ios")
    groups: List[str] = []

    # Contextual metadata — surfaced to the LLM via get_device_info
    site: Optional[str] = None
    role: Optional[str] = None

    @validator("groups", pre=True)
    def ensure_list(cls, v):
        """Accept a bare string as a single-element list."""
        if isinstance(v, str):
            return [v]
        return v


class InventoryIngestRequest(BaseModel):
    """
    Payload for POST /engineer/inventory/ingest.

    Scoped exclusively to the authenticated user (resolved from the API key
    in the router via auth_key.user_id). No assistant_id required or accepted —
    inventory is a user-level resource shared across all assistants belonging
    to that user.
    """

    devices: List[DeviceIngest]
    clear_existing: bool = Field(
        default=False,
        description="If True, wipes the user's existing inventory before ingesting.",
    )


class InventorySearchRequest(BaseModel):
    """
    Payload for group-based inventory searches.
    Scoped to the authenticated user at the service layer.
    """

    group_name: str
