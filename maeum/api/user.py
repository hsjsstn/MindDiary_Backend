from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from maeum.database.database import get_db
from maeum.database import models
from maeum.schemas.user import UserResponse
# UserCreate는 /auth/signup에서 사용

# 라우터 정의
router = APIRouter(prefix="/users", tags=["사용자 API"])

# 회원가입은 /auth/signup 사용

@router.get("/", response_model=list[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    """
    모든 사용자를 조회합니다.
    """
    result = await db.execute(select(models.User))
    users = result.scalars().all()
    return users