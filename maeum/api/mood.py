from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from maeum.database.database import get_db
from maeum.schemas.mood import MonthlyStatisticsRes, WeatherReq, TemperatureRes
from maeum.services.mood_service import statistics_monthly, weather, temperature


router = APIRouter(prefix="/mood", tags=["감정 API"])

@router.get("/statistics/monthly", response_model=MonthlyStatisticsRes)
async def get_statistics_monthly(
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Query(...),
    year: int = Query(...),
    month: int = Query(..., ge=1, le=12)
) :
    statistics_monthly_result = await statistics_monthly(db, user_id, year, month)
    return statistics_monthly_result

@router.post("/weather")
async def post_weather(
    req: WeatherReq,
    db: AsyncSession = Depends(get_db), 
) :
    await weather(db, req.user_id, 7)

    return Response(status_code=204)

@router.get("/temperature", response_model=TemperatureRes)
async def get_temperature(
    user_id: UUID =Query(...),
    db: AsyncSession=Depends(get_db)
):
    temperature_result=await temperature(db, user_id)
    return temperature_result