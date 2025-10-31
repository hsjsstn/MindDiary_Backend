from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import extract, select, and_
from datetime import date
from typing import Optional
from uuid import UUID
import uuid

from maeum.database.models import MoodTemperature

async def create_mood_temperature(
        db: AsyncSession, 
        user_id: UUID, 
        temperature: float,
        threshold_breach: bool,
        ):
    new_temperature = MoodTemperature( 
        temp_id = uuid.uuid4(),
        user_id = user_id,
        entry_date = date.today(),
        temperature = temperature,
        threshold_breach = threshold_breach,

    )
    await db.add(new_temperature)
    await db.commit()
    await db.refresh(new_temperature)

    return new_temperature

async def read_mood_temperature(
        db: AsyncSession,
        user_id: UUID
        
) -> Optional[MoodTemperature]:
    stmt = (
        select(MoodTemperature)
        .where(MoodTemperature.user_id== user_id)
        .order_by(
            MoodTemperature.entry_date.desc(),
            MoodTemperature.created_at.desc()
        )
        .limit(1)
    )

    res = await db.execute(stmt)
    return res.scalars().first()