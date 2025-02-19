from typing import Optional

from pydantic import BaseModel, TypeAdapter
from datetime import datetime


class Image(BaseModel):
    id: int
    name: str
    creation_date: datetime
    deletion_date: Optional[datetime] = None
    active_flag: bool
    status: str
    uuid: str
    description: str
    notes: str
    public: bool
    cloud_image: bool
    so_base: str
    required_disk: int
    api_version: str
    api_version_value: int
    version: str


ImageListAdapter = TypeAdapter(list[Image])
