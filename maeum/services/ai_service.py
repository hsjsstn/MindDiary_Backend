from fastapi import HTTPException
import os, re, json
from pydantic import BaseModel, Field
from groq import Groq
from dotenv import load_dotenv
from maeum.schemas.ai import DiaryReq, Emotions, ReportRes
from maeum.core.config import settings

async def make_report(req: DiaryReq):

    client = settings.client

    REP_SYS = (
            "너는 일기를 분석하는 심리 코치다. "
            "반드시 JSON으로만 답하라. "
            "출력 형식:\n"
            "{\n"
            "    \"mood\": \"대표 감정 하나 (행복/쏘쏘/불안/화남/슬픔 중 하나)\",\n"
            "    \"emotions\": {\n"
            "       \"행복\": 0-100,\n"
            "       \"쏘쏘\": 0-100,\n"
            "       \"불안\": 0-100,\n"
            "       \"화남\": 0-100,\n"
            "       \"슬픔\": 0-100\n"
            "    }\n"
            "}\n"
            "※ 반드시 위 다섯 감정만 포함해라."
            )
    
    try:
        report_res = client.chat.completions.create (
            messages=[
                {"role": "system", "content":  REP_SYS},
                {"role": "user", "content": req.content}
            ],
            model="openai/gpt-oss-120b",
            temperature=0,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,
            stop=None

            )
        raw = report_res.choices[0].message.content
        data = json.loads(raw)

        emo = data.get("emotions", {}) or {}
        normalized = {
            "행복": int(emo.get("행복", 0)),
            "쏘쏘": int(emo.get("쏘쏘", 0)),
            "불안": int(emo.get("불안", 0)),
            "화남": int(emo.get("화남", 0)),
            "슬픔": int(emo.get("슬픔", 0)),
        }
        mood = data.get("mood", "")

        return {"mood": mood, "emotions": normalized}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq 호출 실패: {e}")    
