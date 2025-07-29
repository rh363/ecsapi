from typing import List

from pydantic import BaseModel, TypeAdapter, BeforeValidator
from typing_extensions import Annotated


class Region(BaseModel):
    id: int
    location: str
    description: str


RegionListAdapter = TypeAdapter(List[Region])


class _RegionListResponse(BaseModel):
    status: str
    regions: List[Region]


class _RegionAvailableRequest(BaseModel):
    plan: str


def decomprime_regions(value):
    if not isinstance(value, list):
        return value
    if len(value) == 0 or not isinstance(value[0], list):
        return value
    return value[0]


class _RegionAvailableResponse(BaseModel):
    status: str
    regions: Annotated[List[str], BeforeValidator(decomprime_regions)]
