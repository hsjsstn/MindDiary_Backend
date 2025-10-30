from pydantic import BaseModel
from typing import List, Dict
import re, unicodedata
from maeum.schemas.help import RiskReq, Trigger, RiskRes

RISK_KEYWORDS = [
    "죽고 싶", "다 끝내고 싶", "사라지고 싶", "없어지고 싶",
    "차라리 죽었으면", "영원히 잠들고 싶", "자살하고 싶", "극단적 선택",
    "유서", "작별 인사", "투신", "음독", "번개탄", "칼", 
    "약 먹고", "수면제", "진통제", "옥상", "철로", "고층",
    "우울", "무기력", "외롭", "의미 없", "아무것도 하기 싫"
    "자살", 
]

def normalize_text(text: str) -> str:
    return unicodedata.normalize("NFKC", text).lower()

def detect_keyworkds(text: str) -> Dict[str, int]:
    norm = normalize_text(text)
    counts = {}
    for kw in RISK_KEYWORDS:
        pattern = re.escape(kw).replace(r"\ ", r"\s*")
        matches = re.findall(pattern, norm)
        if matches:
            counts[kw] = len(matches)
    return counts

async def detect_risk(req: RiskReq):
    counts = detect_keyworkds(req.content)
    total = sum(counts.values())
    detected = total >= 5
    triggers = [Trigger(keyword=k, count=v) for k, v in counts.items()]
    return {"detected": detected, "total_count": total, "triggers": triggers}