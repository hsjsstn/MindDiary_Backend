from pydantic import BaseModel, Field
from typing import Optional

class DiaryReq(BaseModel):
    content: str
    name: str

class Emotions(BaseModel):
    행복: int = Field(ge=0, le=100)
    쏘쏘: int = Field(ge=0, le=100)
    불안: int = Field(ge=0, le=100)
    화남: int = Field(ge=0, le=100)
    슬픔: int = Field(ge=0, le=100)

class ReportRes(BaseModel):
    mood: str
    emotions: Emotions    
    