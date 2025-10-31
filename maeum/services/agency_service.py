# maeum/services/agency_service.py (Async 버전으로 수정)

from sqlalchemy.ext.asyncio import AsyncSession # AsyncSession으로 변경
from maeum.crud.agency import get_all_agencies_async # 비동기 CRUD 함수 import
from maeum.schemas.agency import HelpPopupResponse, HelpAgencyBase
from typing import List

# 함수 시그니처를 비동기로 변경
async def check_for_help_popup_db_async(db: AsyncSession, overall_weather_score: float, has_danger_word: bool) -> HelpPopupResponse:
    """
    마음 날씨 점수 및 위험어 탐지 결과를 기반으로 팝업 필요성을 판단하고 응답 객체를 생성합니다.
    """
    
    popup_needed = overall_weather_score <= 25.0 or has_danger_word
    reason = "마음 날씨 점수가 낮거나 일기에서 위험어가 탐지되었습니다. 도움 기관 정보를 확인해보세요." if popup_needed else "마음 날씨가 양호합니다."
    
    agencies: List[HelpAgencyBase] = []
    
    if popup_needed:
        # 비동기 CRUD 함수 호출 시 await 사용
        db_agencies = await get_all_agencies_async(db) 
        
        # Pydantic 모델로 변환
        agencies = [HelpAgencyBase.model_validate(agency) for agency in db_agencies]

    return HelpPopupResponse(
        popup_needed=popup_needed,
        reason=reason,
        agencies=agencies
    )