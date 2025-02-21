from enum import Enum
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, TypeAdapter


class ActionStatusEnum(str, Enum):
    completed = "completed"
    failed = "failed"
    in_progress = "in-progress"


class Action(BaseModel):
    id: int
    status: str
    user: str
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    resource: str
    resource_type: str
    type: str
    progress: int


ActionListAdapter = TypeAdapter(List[Action])


class _ActionListResponse(BaseModel):
    status: str
    actions: List[Action]
    total_actions: int


class _ActionRetrieveResponse(BaseModel):
    status: str
    action: Action
