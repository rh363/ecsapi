from typing import Optional, List

from pydantic import BaseModel, TypeAdapter, field_validator, Field


class CloudScript(BaseModel):
    id: int
    user: Optional[str]
    title: str
    content: str
    windows: bool
    public: bool
    category: Optional[str] = None


CloudScriptListAdapter = TypeAdapter(List[CloudScript])


class _CloudScriptListResponse(BaseModel):
    status: str
    scripts: List[CloudScript]


class _CloudScriptRetrieveResponse(BaseModel):
    status: str
    script: CloudScript


class _CloudScriptCreateRequest(BaseModel):
    title: Optional[str] = Field(default="by ecsapi")
    content: Optional[str] = Field(default="by ecsapi")
    windows: bool = False

    @field_validator("title", "content", mode="before")
    @classmethod
    def set_default(cls, v):
        return v or "by ecsapi"


class _CloudScriptCreateResponse(BaseModel):
    status: str
    script: CloudScript


class _CloudScriptUpdateRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    windows: Optional[bool] = None


_CloudScriptUpdateResponse = _CloudScriptCreateResponse
