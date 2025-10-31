import uvicorn
from fastapi import FastAPI
# maum/api/endpoints/ai.py 파일의 라우터를 직접 임포트
from maeum.api.ai import router as ai_router 
from maeum.api.help import router as help_router
from maeum.api.agency import router as agency_router
from maeum.api.journal import router as journal_router
from maeum.api.user import router as user_router
from maeum.api.auth import router as auth_router
from maeum.api.mood import router as mood_router

# maum/database.database의 engine과 Base 임포트 (DB 초기화에 필요)
# from maeum.database.database import engine, Base
# from maeum.database import models  

app = FastAPI(title="마음일기 백엔드 API")

import asyncio
from maeum.database.database import engine, Base

@app.on_event("startup")
async def startup_event():
    # 테이블 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 기존 테이블에 password 컬럼 추가(마이그레이션)
    import aiosqlite
    import os
    db_path = "./test.db" if os.path.exists("./test.db") else "../test.db"
    try:
        async with aiosqlite.connect(db_path) as db:
            cursor = await db.execute("PRAGMA table_info(user)")
            columns = [row[1] for row in await cursor.fetchall()]
            if 'password' not in columns:
                await db.execute("ALTER TABLE user ADD COLUMN password TEXT DEFAULT ''")
                await db.commit()
                print("password 컬럼이 추가되었습니다.")
    except Exception as e:
        print(f"마이그레이션 중 오류 (무시 가능): {e}")

# DB 초기화 로직 (startup 이벤트)
# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# user 라우터 연결
app.include_router(user_router, prefix="", tags=["User API"])

# 인증 라우터 연결 (회원가입/로그인)
app.include_router(auth_router, prefix="", tags=["인증 API"])

# --- AI 라우터 직접 연결 ---
# '/ai' 경로 접두사 없이 연결할 수 있지만, 여기서는 /ai 경로를 갖는다고 가정합니다.

app.include_router(ai_router, prefix="", tags=["AI 처리 API"])

app.include_router(help_router, prefix="", tags=["위험 상황 알림 API"])

# 도움 기관 라우터 연결
app.include_router(agency_router, prefix="", tags=["도움 기관 API"])

# Journal 라우터 추가
app.include_router(journal_router, prefix="", tags=["일기 처리 API"])

# 감정 라우터 연결
app.include_router(mood_router, prefix="", tag=["감정 API"])

