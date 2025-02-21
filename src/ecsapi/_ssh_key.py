from typing import List

from pydantic import BaseModel, TypeAdapter
from datetime import datetime


class SshKey(BaseModel):
    id: int
    key: str
    label: str
    created_at: datetime


SshKeyListAdapter = TypeAdapter(List[SshKey])


class _SshKeyListResponse(BaseModel):
    status: str
    pubkeys: List[SshKey]


class _SshKeyRetrieveResponse(BaseModel):
    status: str
    pubkey: SshKey


class _SshKeyCreateRequest(BaseModel):
    key: str
    label: str


class _SshKeyCreateResponse(BaseModel):
    status: str


class _SshKeyUpdateRequest(BaseModel):
    label: str


class _SshKeyUpdateResponse(BaseModel):
    status: str
    pubkey: SshKey


class _SshKeyDeleteResponse(BaseModel):
    status: str
