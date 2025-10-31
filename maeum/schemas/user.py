from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

# 사용자 생성을 위한 요청 스키마 (회원가입)
class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="사용자 이메일 (고유값)")
    nickname: str = Field(..., min_length=1, description="사용자 닉네임 (중복 허용)")
    password: str = Field(..., min_length=6, description="비밀번호 (최소 6자)")
    
# 로그인 요청 스키마
class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="이메일")
    password: str = Field(..., description="비밀번호")

# 사용자 응답 스키마
class UserResponse(BaseModel):
    user_id: UUID
    email: str
    nickname: str
    created_at: datetime

    class Config:
        from_attributes = True

# 로그인 응답 스키마 (사용자 정보만 반환)
LoginResponse = UserResponse
