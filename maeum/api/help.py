from fastapi import APIRouter
from maeum.schemas.help import RiskReq, RiskRes, Trigger
from maeum.services import help_service

router = APIRouter(prefix="/help", tags=["위험 상황 알림 API"])

@router.post("/detect-risk", response_model=RiskRes)
async def post_detect_risk( 
    req: RiskReq,
):
    detect_risk_result = await help_service.detect_risk(req)

    return detect_risk_result