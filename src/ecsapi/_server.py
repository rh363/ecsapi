import re
from enum import Enum

from pydantic import (
    BaseModel,
    TypeAdapter,
    Field,
    field_validator,
    model_validator,
    ValidationInfo,
)
from typing import Optional, Union, List, Literal
from typing_extensions import Self
from datetime import datetime

from ._action import Action
from ._discount_record import DiscountRecord
from ._server_support import ServerSupport
from ._snapshot import Snapshot


class ServerStatusEnum(str, Enum):
    booting = "Booting"
    booted = "Booted"
    deleting = "Deleting"
    deleted = "Deleted"
    reimaging = "Reimaging"
    fail = "Fail"
    customizing = "Customizing"


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


ServerListAdapter = TypeAdapter(List[Server])


class _ServerListResponse(BaseModel):
    status: str
    count: int
    server: List[Server]


class _ServerRetrieveResponse(BaseModel):
    status: str
    server: Server


class _ServerRetrieveStatusServerResponse(BaseModel):
    name: str
    current_status: str


class _ServerRetrieveStatusResponse(BaseModel):
    status: str
    server: _ServerRetrieveStatusServerResponse


class ServerCreateRequestNetworkVlan(BaseModel):
    vlan_id: Optional[int] = None
    pvid: Optional[bool] = None
    vlans: Optional[str] = None

    @model_validator(mode="after")
    def check_mutually_exclusive(self) -> Self:
        if self.vlan_id is None and self.vlans is None:
            raise ValueError("one of vlan_id or vlans must be provided")
        if self.vlan_id is not None and self.vlans is not None:
            raise ValueError("vlan_id and vlans are mutually exclusive")
        return self

    @field_validator("vlans")
    @classmethod
    def validate_vlans(cls, v, info: ValidationInfo):
        if v is not None:
            pattern = "^([1-4]?[0-9]?[0-9]?[0-9]?).-([1-4]?[0-9]?[0-9]?[0-9]).?"
            match_pattern = re.search(pattern, v)
            assert match_pattern, f"vlans field must match 1-4094 pattern `{pattern}`"
            start, end = v.split("-")
            start_int = int(start)
            end_int = int(end)
            valid_start = 0 < start_int < 4094 and start_int < end_int
            valid_end = 1 < end_int < 4095 and end_int > start_int
            assert (
                valid_start
            ), "valid start digit of vlans must match `0 < start < 4094` and must be < of end"
            assert (
                valid_end
            ), "valid end digit of vlans must match `1 < end < 4095` and must be > of start"
        return v


class ServerCreateRequestNetwork(BaseModel):
    name: str
    vlans: List[ServerCreateRequestNetworkVlan]


class ServerCreateRequest(BaseModel):
    plan: str
    image: str
    location: str
    notes: Optional[str] = Field(default="created by ecsapi")
    password: Optional[str] = None
    reserved_plan: Optional[str] = None
    support: Optional[str] = None
    group: Optional[str] = None
    user_customize: Optional[Union[str, int]] = None
    user_customize_env: Optional[str] = None
    ssh_key: Optional[str] = None
    networks: Optional[List[ServerCreateRequestNetwork]] = None
    isolate_from: Optional[List[str]] = None

    @field_validator("notes", mode="before")
    @classmethod
    def set_default(cls, v):
        return v or "created by ecsapi"

    @model_validator(mode="after")
    def check_mutually_exclusive(self) -> Self:
        if self.user_customize_env is not None:
            if self.user_customize is None:
                raise ValueError("cant use user_customize_env without user_customize")
            if not isinstance(self.user_customize, int):
                raise ValueError(
                    "cant use user_customize_env if user_customize is not an int"
                )
        return self


class _ServerCreateRequestResponse(BaseModel):
    status: str
    action_id: int
    server: Server


class _ServerUpdateRequest(BaseModel):
    notes: Optional[str] = None
    group: Optional[str] = None


class _ServerActionRequest(BaseModel):
    type: Literal["rollback", "console", "power_on", "power_off"]
    snapshot: Optional[int] = None


class _ServerDeleteResponse(BaseModel):
    status: str
    action: Action
