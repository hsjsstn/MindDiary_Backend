from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract, and_
from datetime import date
import calendar
from statistics import mean
from collections import defaultdict
import random
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from maeum.schemas.mood import MonthlyStatisticsRes, PieChart, WeeklyItem
from maeum.crud.journal_analysis import read_analysis_by_month, read_analysis_recent_n
from maeum.crud.mood_temperature import read_mood_temperature

EMOS = ["happy", "soso", "anxiety", "anger", "sadness"]
LABELS = ["행복", "쏘쏘", "불안", "화남", "슬픔"]
EMO_KR = {
    "happy": "행복",
    "soso": "쏘쏘",
    "anxiety": "불안",
    "anger": "화남",
    "sadness": "슬픔",
}

RECOMMENDATIONS = {
    "happy": [
            "오늘의 좋은 순간을 짧게 기록하세요(3줄 일기).",
            "가벼운 산책 15분으로 긍정 상태를 연장하세요.",
            "좋아하는 노래를 들어보세요.",
            "다음 주에 기대되는 일 1가지를 구체적으로 계획하고 적어보세요.",
            "자신이 잘 해낸 일 3가지를 구체적인 이유와 함께 기록하세요."
        ],
    "soso": [
            "하루 루틴을 10%만 바꿔보세요.",
            "‘괜찮았던 점 3가지’를 적어보세요.",
            "오늘 하루 감사했던 일이 있나요? 사소한거라도 좋으니 떠올려봐요!",
            "일상생활 속 새로운 것 1가지를 찾아보세요.",
            "간단한 그림이나 낙서를 10분동안 하며 손을 사용해보세요.",
            "단기 목표 1개를 정하고 달성 시 자신에게 줄 보상을 구체적으로 정해보세요."
        ],
    "anxiety": [
            "4-7-8 호흡을 3세트 해보세요.",
            "불안을 느끼는 신체 부위에 손을 얹고 따뜻한 감각에 집중하세요.",
            "지금의 불안을 객관적으로 '이름붙여' 말해보세요. 감정명명은 감정의 감도를 감소시킬 수 있습니다.",
            "걱정되는 생각에 대해 '이 생각은 사실인가?'를 따져보세요.",
            "'만약 최악의 상황이 발생하면 어떻게 대쳐할 것인가?'를 미리 적어보고 대안을 2개이상 만들어 보세요."
        ],
    "anger": [
            "빠른 걷기 10분으로 긴장을 빼주세요.",
            "감정을 ‘사실/느낌/요구’로 분리해 1문장씩 적어보세요.",
            "분노를 유발한 상황에 대해 '다른 사람의 관점'에서 생각해보세요.",
            "종이에 분노의 대상을 그림이나 상징으로 그린 후 찢거나 구겨서 버려보세요.",
            "분노를 느끼는 상황이 올 때 잠깐 분노를 멈출 수 있도록 노력해봐요."
        ],
    "sadness": [
            "따뜻한 물로 샤워 후 5분 스트레칭헤보세요.",
            "친한 사람 1명에게 근황 연락을 보내보는 건 어떨까요?.",
            "가장 하기 쉬운 집안일 1개만 정하고 10분 동안 완료하세요.",
            "슬픔을 유발하는 상황이 영원히 지속되지 않을 것임을 스스로에게 상기시키세요.",
            "자신에게 비난하는 말을 할 때, '가장 친한 친구에게도 이 말을 할 것인가?'라고 자문해보세요.",
            "잔잔한 음악을 들으며 10분간 색칠 공부나 퍼즐 맞추기 등 단순 반복 활동을 하세요.",
            "따뜻한 담요를 덮고 편안한 자세로 10분간 휴식을 취해보세요.",
            "햇볕이 잘 드는 곳에서 20분간 머물러봐요."
        ],
}

def week_of_month(d: date) -> int:
    return (d.day-1)//7 +1

async def statistics_monthly(
        db: AsyncSession,
        user_id: UUID, 
        year: int, 
        month: int) -> MonthlyStatisticsRes:
    analyses = await read_analysis_by_month(db, user_id, year, month)

    last_day = calendar.monthrange(year, month)[1]
    period = f"{date(year, month, 1).isoformat()} ~{date(year, month, last_day).isoformat()}"

    if not analyses:
        return MonthlyStatisticsRes(
            period=period,
            user_id=user_id,
            total_entries=0,
            dominant_emotion="",
            emotion_avg={k: 0.0 for k in EMOS},
            emotion_pie=PieChart(labels=LABELS, values=[0,0,0,0,0]),
            weekly_dominants=[],
            comment="",
            recommendations=[],
        )
    
    #월 평균 
    emo_vals = {k: [] for k in EMOS}
    for a in analyses:
        emo_vals["happy"].append(a.happy or 0.0)
        emo_vals["soso"].append(a.soso or 0.0)
        emo_vals["anxiety"].append(a.anxiety or 0.0)
        emo_vals["anger"].append(a.anger or 0.0)
        emo_vals["sadness"].append(a.sadness or 0.0)
    emotion_avg = {k: float(mean(v)) if v else 0.0 for k, v in emo_vals.items()}

    #월 대표 감정
    dominant_emotion = EMO_KR[max(emotion_avg, key=emotion_avg.get)]

    #주차별 대표 감정
    weekly_buckets = defaultdict(lambda: {k: [] for k in EMOS})
    for a in analyses:
        w=week_of_month(a.date)
        weekly_buckets[w]["happy"].append(a.happy or 0.0)
        weekly_buckets[w]["soso"].append(a.soso or 0.0)
        weekly_buckets[w]["anxiety"].append(a.anxiety or 0.0)
        weekly_buckets[w]["anger"].append(a.anger or 0.0)
        weekly_buckets[w]["sadness"].append(a.sadness or 0.0)

    weekly_items = []
    for w in sorted(weekly_buckets.keys()):
        wavg = {k: float(mean(v)) if v else 0.0 for k, v in weekly_buckets[w].items()}
        weekly_items.append(WeeklyItem(
            week_index=w,
            dominant_emotion=max(wavg, key=wavg.get)
        ))

    pie = PieChart(
        labels=LABELS,
        values=[emotion_avg["happy"], emotion_avg["soso"], emotion_avg["anxiety"],
                emotion_avg["anger"], emotion_avg["sadness"]]
    )

    comment = f"이번달 대표 감정은 {dominant_emotion}입니다."
    kr_to_en = {v: k for k, v in EMO_KR.items()}
    winner_key = kr_to_en.get(dominant_emotion)
    pool = RECOMMENDATIONS.get(winner_key, [])
    recommendations = random.sample(pool, k=min(2, len(pool))) if pool else []


    return MonthlyStatisticsRes(
        period=period,
        user_id=user_id,
        total_entries=len(analyses),
        dominant_emotion=dominant_emotion,
        emotion_avg=emotion_avg,
        emotion_pie=pie,
        weekly_dominants=weekly_items,
        comment=comment,
        recommendations=recommendations,
    )

async def weather(
        db: AsyncSession,
        user_id: UUID,
        n: int=7
):
    analyses = await read_analysis_recent_n(db, user_id)
    mood_dict = [
        {
            "happy": a.happy,
            "soso": a.soso,
            "anxiety": a.anxiety,
            "anger": a.anger,
            "sadness": a.sadness
        }
        for a in analyses
    ]

    dominant_mood = [max(d, key=d.get) for d in mood_dict]
    yest_temperature = await read_mood_temperature(db, user_id)
    if yest_temperature==None:
        yest_temperature=36.5
    for m in dominant_mood:
        if m=="happy":
            yest_temperature+=2
        elif m =="soso":
            yest_temperature+=1
        elif m=="anxiety":
            yest_temperature-=1
        elif m=="anger":
            yest_temperature-=1
        elif m=="sadness":
            yest_temperature-=2


