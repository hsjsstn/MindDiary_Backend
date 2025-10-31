from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from maeum.database.database import get_db
from maeum.database import models
from maeum.schemas.user import UserCreate, UserResponse, LoginRequest, LoginResponse
import uuid
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["인증 API"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    
    # 이메일 중복 확인 (이메일 중복 비허용)
    email_result = await db.execute(
        select(models.User).where(models.User.email == user_data.email)
    )
    existing_user_email = email_result.scalar_one_or_none()
    if existing_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 존재하는 이메일입니다."
        )
    
    # 비밀번호 저장 (평문으로 저장되어서 추후 해시로 변경 필요)
    # hashed_password = get_password_hash(user_data.password)
    
    # 새 사용자 생성
    new_user = models.User(
        user_id=uuid.uuid4(),
        email=user_data.email,
        nickname=user_data.nickname,
        password=user_data.password,  # 평문 저장
        created_at=datetime.utcnow()
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    로그인 API
    
    이메일과 비밀번호로 사용자를 인증하고 사용자 정보를 반환합니다.
    """
    # 사용자 조회
    result = await db.execute(
        select(models.User).where(models.User.email == login_data.email)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다.",
        )
    
    # 비밀번호 검증 (평문 비교)
    if login_data.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다.",
        )
    
    # 사용자 정보 반환
    return user

