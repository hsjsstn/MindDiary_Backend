from pydantic import BaseModel
from typing import List

class RiskReq(BaseModel):
    content: str

class Trigger(BaseModel):
    keyword: str
    count: int

class RiskRes(BaseModel):
    detected: bool
    total_count: int
    triggers: List[Trigger]
