from fastapi import APIRouter, HTTPException
from typing import List
from pathlib import Path
import json

from maeum.schemas.agency import HelpAgencyBase

router = APIRouter(prefix="/help", tags=["도움 기관 API"])


def _load_agencies_from_json() -> List[HelpAgencyBase]:
    resources_path = Path(__file__).resolve().parents[1] / "resources" / "help_agencies.json"
    if not resources_path.exists():
        raise HTTPException(status_code=500, detail="도움 기관 리소스 파일을 찾을 수 없습니다.")
    try:
        with resources_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return [HelpAgencyBase(name=item.get("name", ""),
                               region=None,
                               phone=item.get("phone", ""),
                               url=item.get("link")) for item in data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"도움 기관 데이터를 불러올 수 없습니다: {e}")


@router.get("/agencies", response_model=List[HelpAgencyBase])
async def list_help_agencies() -> List[HelpAgencyBase]:
    return _load_agencies_from_json()

