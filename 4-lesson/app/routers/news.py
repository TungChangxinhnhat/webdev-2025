# app/routers/news.py
from __future__ import annotations

import json
import logging
from typing import Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.redis import cache_get, cache_set, cache_del

logger = logging.getLogger("cache")
router = APIRouter(prefix="/api", tags=["news"])

# ---- Mô hình dữ liệu (demo in-memory DB) ----
class NewsIn(BaseModel):
    title: str
    body: str

class NewsOut(NewsIn):
    id: int

_DB: Dict[int, Dict[str, str]] = {}
_SEQ: int = 0
TTL_SECONDS = 300  # TTL cache

def _create_in_db(data: NewsIn) -> NewsOut:
    global _SEQ
    _SEQ += 1
    _DB[_SEQ] = data.model_dump()
    return NewsOut(id=_SEQ, **_DB[_SEQ])

def _get_from_db(news_id: int) -> NewsOut:
    raw = _DB.get(news_id)
    if not raw:
        raise HTTPException(status_code=404, detail="Not Found")
    return NewsOut(id= news_id, **raw)

def _update_in_db(news_id: int, data: NewsIn) -> NewsOut:
    if news_id not in _DB:
        raise HTTPException(status_code=404, detail="Not Found")
    _DB[news_id] = data.model_dump()
    return NewsOut(id=news_id, **_DB[news_id])

def _delete_in_db(news_id: int) -> None:
    if news_id not in _DB:
        raise HTTPException(status_code=404, detail="Not Found")
    del _DB[news_id]

# ---- Endpoints ----
@router.post("/news", response_model=NewsOut)
async def create_news(payload: NewsIn):
    item = _create_in_db(payload)
    # tùy chọn: warm cache ngay khi tạo
    await cache_set(f"news:{item.id}", json.dumps(item.model_dump()), ttl=TTL_SECONDS)
    return item

@router.get("/news/{news_id}", response_model=NewsOut)
async def get_news(news_id: int):
    key = f"news:{news_id}"
    if data := await cache_get(key):
        logger.info("CACHE HIT %s", key)
        return NewsOut(**json.loads(data))
    logger.info("CACHE MISS %s", key)
    item = _get_from_db(news_id)
    await cache_set(key, json.dumps(item.model_dump()), ttl=TTL_SECONDS)
    return item

@router.put("/news/{news_id}", response_model=NewsOut)
async def update_news(news_id: int, payload: NewsIn):
    item = _update_in_db(news_id, payload)
    await cache_set(f"news:{news_id}", json.dumps(item.model_dump()), ttl=TTL_SECONDS)
    return item

@router.delete("/news/{news_id}")
async def delete_news(news_id: int):
    _delete_in_db(news_id)
    await cache_del(f"news:{news_id}")
    return {"ok": True}

@router.get("/news", response_model=List[NewsOut])
async def list_news():
    return [NewsOut(id=i, **row) for i, row in sorted(_DB.items())]
