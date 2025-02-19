from pydantic import BaseModel, TypeAdapter
from typing import Optional, Union, List
from datetime import datetime

from ._discount_record import DiscountRecord
from ._server_support import ServerSupport
from ._snapshot import Snapshot


class ServerPlanSize(BaseModel):
    core: str
    ram: str
    disk: str
    gpu: str
    gpu_label: Optional[str] = None
    host_type: str


class Server(BaseModel):
    name: str
    ipv4: str
    ipv6: str
    group: Optional[str] = None
    plan: str
    plan_size: ServerPlanSize
    reserved_plans: List[DiscountRecord]
    last_restored_snapshot: Optional[Snapshot] = None
    is_reserved: bool
    reserved_until: Union[str, datetime]
    support: Optional[ServerSupport] = None
    location: str
    location_label: str
    notes: str
    so: str
    so_label: str
    creation_date: datetime
    deletion_date: Optional[datetime] = None
    active_flag: bool
    status: str
    progress: int
    api_version: str
    api_version_value: int
    user: str
    virttype: Optional[str] = None


ServerListAdapter = TypeAdapter(list[Server])


class _ServerListResponse(BaseModel):
    status: str
    count: int
    server: List[Server]


class _ServerRetrieveResponse(BaseModel):
    status: str
    server: Server
