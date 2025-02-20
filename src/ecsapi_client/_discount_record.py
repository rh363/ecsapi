from typing import List

from pydantic import BaseModel, TypeAdapter
from datetime import datetime


class DiscountRecord(BaseModel):
    reserved_plan: int
    reserved_months: int
    plan: int
    discount: int
    start_date: datetime
    end_date: datetime
    server: str


DiscountRecordListAdapter = TypeAdapter(List[DiscountRecord])
