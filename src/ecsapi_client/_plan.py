from typing import List

from pydantic import BaseModel, TypeAdapter, Field

from ._region import Region


class Plan(BaseModel):
    id: int
    name: str
    cpu: str
    ram: str
    disk: str
    gpu: str
    gpu_label: str
    hourly_price: float
    monthly_price: float = Field(..., alias="montly_price")
    windows: bool
    host_type: str
    available: bool
    available_regions: List[Region]


PlanListAdapter = TypeAdapter(list[Plan])
