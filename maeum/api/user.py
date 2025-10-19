from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from maeum.database.database import get_db
from maeum.database import models
from maeum.schemas.user import UserCreate, UserResponse
import uuid
from datetime import datetime

# 라우터 정의
router = APIRouter(prefix="/users", tags=["User API"])

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    새로운 사용자를 생성합니다.
    """
    # 새로운 UUID를 생성하여 user_id로 사용합니다.
    new_user_id = uuid.uuid4() 
    
    new_user = models.User(
        user_id=new_user_id,
        email=user.email,
        nickname=user.nickname,
        created_at=datetime.utcnow()
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

@router.get("/", response_model=list[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    """
    모든 사용자를 조회합니다.
    """
    result = await db.execute(select(models.User))
    users = result.scalars().all()
    return users