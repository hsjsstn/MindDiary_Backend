from fastapi import HTTPException
import os, re, json
from pydantic import BaseModel, Field
from groq import Groq
from dotenv import load_dotenv

from maeum.schemas.ai import DiaryReq, Emotions, ReportRes, CommentRes, RecommendRes, RecommendReq

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

        return ReportRes(mood=mood, emotions=normalized) #{"mood": mood, "emotions": normalized}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq 호출 실패: {e}")    
    

async def make_comment(req: DiaryReq):
    client = settings.client

    try:
        COM_SYS = (
            "너는 초등학교 선생님 처럼 일기를 읽고 코멘트를 달아야해"
            "최대한 공감과 격려를 하면서 일기에 대한 5~6줄짜리 코멘트 작성해줘."
            f"일기 주인의 이름은 {req.name}이야."
        )
        comment_res = client.chat.completions.create (
        messages=[
            {"role": "system", "content": COM_SYS},
            {"role": "user", "content": req.content}
        ],
        model="openai/gpt-oss-120b",
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None
        )

        comment = comment_res.choices[0].message.content
        return CommentRes(comment=comment) #{"comment": comment}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq 호출 실패: {e}")


async def make_recommend(req: RecommendReq):
    client = settings.client

    try:
        COM_SYS = (
            "너는 월간 일기통계를 분석하는 심리 코치다. "
            "반드시 JSON으로만 답하라. "
            "해당 월의 대표감정, 주차별 대표 감정, 총 일기 수를 통해 종합적으로 분석하여 일기 작성자의 감정의 흐름을 파악해라."
            "출력 형식:\n"
            "{\n"
            "    \"review\": \"해당 월의 감정 통계를 보고 공감과 위로와 격려의 한줄평\",\n"
            "    \"recommend\": \"해당 월의 대표 감정에 대한 행동 추천 3가지\",\n"
            "}\n"
        )
        comment_res = client.chat.completions.create (
        messages=[
            {"role": "system", "content": COM_SYS},
            {"role": "user", "content": (
                f"대표 감정: {req.dominant_mood}\n"
                f"주차별 감정: {[f'{w.week_index}주차: {w.dominant_emotion}' for w in req.weekly_mood]}\n"
                f"총 일기 수: {req.total_journal}"
            )}
        ],
        model="openai/gpt-oss-120b",
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None
        )

        raw = comment_res.choices[0].message.content.strip()

        # JSON 파싱 (GPT가 JSON 외의 문장 섞었을 경우 대비)
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            import re
            json_text = re.search(r'\{[\s\S]*\}', raw)
            if not json_text:
                raise ValueError("GPT 응답에서 JSON을 찾을 수 없음")
            parsed = json.loads(json_text.group())

        # RecommendRes 모델에 매핑
        return RecommendRes(
            review=parsed.get("review", "리뷰 생성 실패"),
            recommend=parsed.get("recommend", "추천 생성 실패")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq 호출 실패: {e}")