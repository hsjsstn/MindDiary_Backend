# maeum/schemas/agency.py
from pydantic import BaseModel, Field
from typing import List, Optional

# 1. 기관 데이터의 기본 형태 (DB에서 읽어오거나 API 응답에 사용)
class HelpAgencyBase(BaseModel):
    name: str = Field(..., description="기관 이름")
    region: Optional[str] = Field(None, description="기관 지역 (없을 수 있음)")
    phone: str = Field(..., description="대표 전화번호")
    url: Optional[str] = Field(None, description="기관 웹사이트 URL (없을 수 있음)")

    class Config:
        from_attributes = True # ORM 모드를 활성화하여 DB 모델과 호환되게 함

# 2. API 응답의 최종 구조 (팝업 필요 여부와 기관 목록 포함)
class HelpPopupResponse(BaseModel):
    popup_needed: bool = Field(..., description="도움 기관 팝업 필요 여부")
    reason: str = Field(..., description="팝업이 필요한 이유 설명")
    agencies: List[HelpAgencyBase] = Field(..., description="제공할 도움 기관 목록")