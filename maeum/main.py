import uvicorn
from fastapi import FastAPI
# maum/api/endpoints/ai.py 파일의 라우터를 직접 임포트
from maeum.api.ai import router as ai_router 
from maeum.api.help import router as help_router
from maeum.api.mood import router as mood_router
# maum/database.database의 engine과 Base 임포트 (DB 초기화에 필요)
# from maeum.database.database import engine, Base
# from maeum.database import models  

app = FastAPI(title="마음일기 백엔드 API")

# DB 초기화 로직 (startup 이벤트)
# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

app.include_router(ai_router, prefix="", tags=["AI 처리 API"])

app.include_router(help_router, prefix="", tags=["위험 상황 알림 API"])

app.include_router(mood_router, prefix="", tags=["감정 API"])