from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import date
from uuid import UUID

class WeeklyItem(BaseModel):
    week_index: int
    dominant_emotion: str

class PieChart(BaseModel):
    labels: List[str]
    values: List[float]

class MonthlyStatisticsRes(BaseModel):
    period: str
    user_id: UUID
    total_entries: int
    dominant_emotion: str
    emotion_avg: Dict[str, float]
    emotion_pie: PieChart
    weekly_dominants: List[WeeklyItem]       
    comment: str        
    recommendations: List[str] = []

class WeatherReq(BaseModel):
    user_id: UUID