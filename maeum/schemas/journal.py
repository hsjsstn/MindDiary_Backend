from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional
from uuid import UUID
from maeum.schemas.agency import HelpPopupResponse

class JournalCreate(BaseModel):
    user_id: Optional[UUID] = Field(None)
    entry_date: date
    content: str

class JournalEntryResponse(BaseModel):
    journal_id: UUID
    entry_date: date
    context: str
    created_at: datetime
    user_id: UUID

    class Config:
        from_attributes = True


class JournalFullResponse(JournalEntryResponse): 
    # AI 분석 관련 필드 (예시)
    overall_weather_score: float = Field(..., description="사용자의 현재 전체 마음 날씨 점수")
    ai_comment_text: str = Field(..., description="AI가 생성한 코멘트")
    
    # 팝업 정보를 담기 위한 필드 추가
    help_popup: HelpPopupResponse = Field(..., description="도움 기관 팝업 필요성 정보")