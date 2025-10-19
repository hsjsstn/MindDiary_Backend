from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

# 사용자 생성을 위한 요청 스키마
class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="사용자 이메일 (고유값)")
    nickname: str = Field(..., min_length=1, description="사용자 닉네임 (고유값)")
    
# 사용자 응답 스키마
class UserResponse(BaseModel):
    user_id: UUID
    nickname: str
    created_at: datetime

    class Config:
        from_attributes = True
