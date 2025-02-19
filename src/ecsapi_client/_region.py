from pydantic import BaseModel, TypeAdapter


class Region(BaseModel):
    id: int
    location: str
    description: str


RegionListAdapter = TypeAdapter(list[Region])
