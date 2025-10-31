# maeum/crud/agency.py (Async 버전으로 수정)

from sqlalchemy.ext.asyncio import AsyncSession # AsyncSession import
from sqlalchemy.future import select # select import
from typing import List
from maeum.database.models import HelpAgency

# 모든 도움 기관 정보를 가져오는 비동기 함수
async def get_all_agencies_async(db: AsyncSession) -> List[HelpAgency]:
    # 비동기 세션을 사용
    result = await db.execute(select(HelpAgency))
    return result.scalars().all()