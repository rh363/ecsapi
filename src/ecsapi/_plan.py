from typing import List, Optional

from pydantic import BaseModel, TypeAdapter, Field

from ._image import Image
from ._region import Region


class Plan(BaseModel):
    id: int
    name: str
    cpu: str
    ram: str
    disk: str
    gpu: Optional[str] = None
    gpu_label: Optional[str] = None
    hourly_price: float
    monthly_price: float = Field(..., alias="montly_price")
    windows: bool
    host_type: str
    available: bool
    default_image: Optional[str] = None
    available_regions: List[Region]


PlanListAdapter = TypeAdapter(list[Plan])


class _PlanListResponse(BaseModel):
    status: str
    plans: List[Plan]


class _PlanAvailableRegionAvailableHostServer(BaseModel):
    name: str
    notes: str


class _PlanAvailableRegionAvailableHost(BaseModel):
    host: str
    servers: Optional[list[_PlanAvailableRegionAvailableHostServer]] = Field(
        default_factory=list
    )


class _PlanAvailableRegionAvailable(BaseModel):
    region: str
    hosts: list[_PlanAvailableRegionAvailableHost]


class _PlanAvailable(BaseModel):
    id: int
    name: str
    cpu: str
    ram: str
    disk: str
    gpu: Optional[str] = None
    gpu_label: Optional[str] = None
    hourly_price: float
    monthly_price: float = Field(..., alias="montly_price")
    windows: bool
    host_type: str
    available: bool
    default_image: Optional[str] = None
    os_available: List[Image] = Field(..., alias="os_availables")
    region_available: List[_PlanAvailableRegionAvailable] = Field(
        ..., alias="region_availables"
    )
    runtimeclass: Optional[str] = None


class _PlanAvailableListResponse(BaseModel):
    status: str
    plans: List[_PlanAvailable]
