from enum import Enum
from typing import Optional, List
from typing_extensions import Self
from pydantic import BaseModel, TypeAdapter, model_validator, Field, field_validator
from datetime import datetime

from ._action import Action


class ImageStatusEnum(str, Enum):
    creating = "CG"
    created = "CD"
    deleting = "DE"
    deleted = "DD"
    fail = "FL"


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


ImageListAdapter = TypeAdapter(List[Image])


class _ImageListResponse(BaseModel):
    status: str
    images: List[Image]


_CloudImageListResponse = _ImageListResponse


class _TemplateListResponse(BaseModel):
    status: str
    templates: List[Image]


class _TemplateRetrieveResponse(BaseModel):
    status: str
    template: Image


class _TemplateCreateRequest(BaseModel):
    notes: Optional[str] = Field(default="created by ecsapi")
    description: Optional[str] = Field(default="created by ecsapi")
    snapshot: Optional[int] = None
    server: Optional[str] = None

    @field_validator("notes", "description", mode="before")
    @classmethod
    def set_default(cls, v):
        return v or "created by ecsapi"

    @model_validator(mode="after")
    def check_mutually_exclusive(self) -> Self:
        if self.snapshot is None and self.server is None:
            raise ValueError("one of snapshot or server must be provided")
        if self.snapshot is not None and self.server is not None:
            raise ValueError("snapshot and server are mutually exclusive")
        return self


class _TemplateCreateResponse(BaseModel):
    status: str
    action_id: int
    template: Image


class _TemplateUpdateRequest(BaseModel):
    notes: Optional[str] = None
    description: Optional[str] = None


_TemplateUpdateResponse = _TemplateRetrieveResponse


class _TemplateDeleteResponse(BaseModel):
    status: str
    action: Action
