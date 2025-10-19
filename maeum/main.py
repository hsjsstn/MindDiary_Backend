import uvicorn
from fastapi import FastAPI
# maum/api/endpoints/ai.py 파일의 라우터를 직접 임포트
from maeum.api.ai import router as ai_router 
<<<<<<< Updated upstream
=======
from maeum.api.help import router as help_router
from maeum.api.journal import router as journal_router
from maeum.api.user import router as user_router
>>>>>>> Stashed changes
# maum/database.database의 engine과 Base 임포트 (DB 초기화에 필요)
# from maeum.database.database import engine, Base
# from maeum.database import models  

app = FastAPI(title="마음일기 백엔드 API")

import asyncio
from maeum.database.database import engine, Base

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# DB 초기화 로직 (startup 이벤트)
# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# user 라우터 연결
app.include_router(user_router, prefix="", tags=["User API"])

# --- AI 라우터 직접 연결 ---
# '/ai' 경로 접두사 없이 연결할 수 있지만, 여기서는 /ai 경로를 갖는다고 가정합니다.
app.include_router(ai_router, prefix="", tags=["AI 처리 API"])
<<<<<<< Updated upstream
=======

app.include_router(help_router, prefix="", tags=["위험 상황 알림 API"])

# Journal 라우터 추가
app.include_router(journal_router, prefix="", tags=["일기 처리 API"])
>>>>>>> Stashed changes
