from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from maeum.database.database import get_db
from maeum.database import models
from maeum.schemas.journal import JournalCreate, JournalEntryResponse
import uuid
from datetime import datetime


router = APIRouter(prefix="/journals", tags=["Journal API"])

@router.post("/", response_model=JournalEntryResponse)
async def create_journal(journal: JournalCreate, db: AsyncSession = Depends(get_db)):
    new_entry = models.JournalEntry(
        journal_id=uuid.uuid4(),
        user_id=journal.user_id,
        entry_date=journal.entry_date,
        context=journal.content,
        created_at=datetime.utcnow()
    )
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)
    return new_entry

@router.get("/", response_model=list[JournalEntryResponse])
async def get_journals(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.JournalEntry))
    journals = result.scalars().all()
    return journals
