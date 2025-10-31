from fastapi import APIRouter
from maeum.schemas.ai import DiaryReq, Emotions, ReportRes, CommentRes
from maeum.services import ai_service # 위에서 만든 서비스 임포트
from maeum.database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

router = APIRouter(prefix="/ai", tags=["AI 처리 API"])

@router.post("/diaryemotion-analysis", response_model=ReportRes)
async def post_diaryemotion_analysis(
    req: DiaryReq,
    # db: AsyncSession = Depends(get_db)
):
    analysis_result = await ai_service.make_report(req)

    return analysis_result  

@router.post("/generate-comment", response_model=CommentRes)
async def post_generate_commnet(
    req: DiaryReq,

):
    commnet_result = await ai_service.make_comment(req)

    return commnet_result
