from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import extract, select, and_
import datetime
from typing import List, Tuple
from uuid import UUID
import uuid

from maeum.database.models import JournalAnalysis, JournalEntry
from maeum.schemas.ai import ReportRes

def create_journal_analysis(db: AsyncSession, journal_id: UUID, data: ReportRes):
    # """JournalAnalysis 테이블에 새 분석 결과 저장"""
    emotions = data.emotions.dict()

    mapping = {
        "행복" : "happy",
        "쏘쏘" : "soso",
        "불안": "anxiety",
        "화남": "anger",
        "슬픔": "sadness"
    }

    new_analysis = JournalAnalysis (
        analysis_id = uuid.uuid4(),
        date = datetime.date.today(),
        journal_id = journal_id,
        **{mapping[k]: v for k, v in emotions.items()}
    )

    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    return new_analysis

async def read_analysis_by_month(
        db: AsyncSession,
        user_id: UUID,
        year: int,
        month: int
) -> List[JournalAnalysis]:
    # star, end = month_range(year, month)
    stmt = (
        db.query(JournalAnalysis)
        .join(JournalEntry, JournalAnalysis.journal_id == JournalEntry.journal_id)
        .where(JournalEntry.user_id == user_id)
        .where(extract('year', JournalAnalysis.date) == year)
        .where(extract('month', JournalAnalysis.date) == month)
        .all()
    )
    res = await db.execute(stmt)

    return res.scalars().all()

async def read_analysis_recent_n(
        db: AsyncSession,
        user_id: UUID,
        n: int = 7,
) -> List[JournalAnalysis]:
    
    query = (
        select(JournalAnalysis)
        .join(JournalEntry, JournalAnalysis.journal_id==JournalEntry.journal_id)
        .where(JournalEntry.user_id == user_id)
        .order_by(JournalAnalysis.date.desc(), JournalAnalysis.analysis_id.desc())
        .limit(n)   
    )
    res = await db.execute(query)
    rows = res.scalars().all()

    return list(reversed(rows))