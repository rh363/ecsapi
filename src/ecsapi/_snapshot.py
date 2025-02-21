from pydantic import BaseModel, TypeAdapter
from typing import Optional, List
from datetime import datetime


class Snapshot(BaseModel):
    id: int
    name: str
    user: str
    snapshot_parent: "Optional[Snapshot]" = None
    snapshot_parent_name: "Optional[str]" = None
    is_last_restored: bool
    protected: bool
    restoring: bool
    source_server: str
    status: str
    status_label: str
    uid: str
    description: str
    notes: str
    active_flag: bool
    size_on_disk: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    api_version_value: int
    api_version: str


SnapshotListAdapter = TypeAdapter(List[Snapshot])
