import uvicorn
from fastapi import FastAPI
from maeum.api.ai import router as ai_router 
from maeum.api.help import router as help_router
from maeum.api.agency import router as agency_router
from maeum.api.journal import router as journal_router
from maeum.api.user import router as user_router
from maeum.api.auth import router as auth_router
from maeum.api.mood import router as mood_router
from dotenv import load_dotenv
load_dotenv()

# maum/database.database의 engine과 Base 임포트 (DB 초기화에 필요)
# from maeum.database.database import engine, Base
# from maeum.database import models  

app = FastAPI(title="마음일기 백엔드 API")

import asyncio
from maeum.database.database import engine, Base

# DB 초기화 로직 (startup 이벤트)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# user 라우터 연결
app.include_router(user_router)

# 인증 라우터 연결 (회원가입/로그인)
app.include_router(auth_router)

# --- AI 라우터 직접 연결 ---
# '/ai' 경로 접두사 없이 연결할 수 있지만, 여기서는 /ai 경로를 갖는다고 가정합니다.

app.include_router(ai_router)

app.include_router(help_router)

app.include_router(mood_router)

app.include_router(journal_router)
