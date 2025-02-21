from pydantic import BaseModel, TypeAdapter, Field
from typing import Optional, List
from datetime import datetime


class ServerSupport(BaseModel):
    server_name: str = Field(..., alias="server__name")
    server_notes: str
    support_title: str
    support_code: str
    immutable: bool
    start: datetime
    end: Optional[datetime] = None
    may_downgrade: bool
    weight: int = Field(..., alias="weigth")
    days: int
    cancelled: bool
    cancelled_at: Optional[datetime] = None


ServerSupportListAdapter = TypeAdapter(List[ServerSupport])
