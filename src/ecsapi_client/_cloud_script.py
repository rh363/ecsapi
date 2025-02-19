from typing import Optional

from pydantic import BaseModel, TypeAdapter


class CloudScript(BaseModel):
    id: int
    user: Optional[str]
    title: str
    content: str
    windows: bool
    public: bool
    category: str


CloudScriptListAdapter = TypeAdapter(list[CloudScript])
