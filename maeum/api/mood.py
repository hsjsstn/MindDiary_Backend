from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from maeum.database.database import get_db
from maeum.schemas.mood import MonthlyStatisticsRes, WeatherReq
from maeum.services.mood_service import statistics_monthly, weather


router = APIRouter(prefix="/mood", tags=["감정 API"])

@router.get("/statistics/monthly", response_model=MonthlyStatisticsRes)
async def statistics_monthly(
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Query(...),
    year: int = Query(...),
    month: int = Query(..., ge=1, le=12)
) :
    statistics_monthly_result = await statistics_monthly(db, user_id, year, month)
    return statistics_monthly_result

@router.post("/weather")
async def post_weather(
    db: AsyncSession = Depends(get_db),
    req: WeatherReq
) :
    await weather(db, req.user_id, 7)

    return Response(status_code=204)