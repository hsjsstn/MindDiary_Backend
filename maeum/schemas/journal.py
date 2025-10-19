from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional
from uuid import UUID

class JournalCreate(BaseModel):
    user_id: Optional[UUID] = Field(None)
    entry_date: date
    content: str

class JournalEntryResponse(BaseModel):
    journal_id: UUID
    entry_date: date
    context: str
    created_at: datetime
    user_id: UUID

    class Config:
        from_attributes = True