from sqlalchemy.orm import Session
from sqlalchemy import extract
import datetime
from typing import List, Tuple
from uuid import UUID
import uuid

from maeum.database.models import JournalAnalysis, JournalEntry
from maeum.schemas.ai import ReportRes

def create_journal_analysis(db: Session, journal_id: UUID, data: ReportRes):
    """JournalAnalysis 테이블에 새 분석 결과 저장"""
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

def read_analysis_by_month(
        db: Session,
        user_id: UUID,
        year: int,
        month: int
) -> List[JournalAnalysis]:
    # star, end = month_range(year, month)
    analysis = (
        db.query(JournalAnalysis)
        .join(JournalEntry, JournalEntry.journal_id == JournalEntry.journal_id)
        .filter(JournalEntry.user_id == user_id)
        .filter(extract('year', JournalAnalysis.date) == year)
        .filter(extract('month', JournalAnalysis.date) == month)
        .all()
    )

    return analysis