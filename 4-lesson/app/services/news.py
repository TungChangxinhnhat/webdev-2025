import json
import os
from typing import List
from app.models import News  # SQLAlchemy model
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.redis import get_redis

NEWS_CACHE_TTL = int(os.getenv("NEWS_CACHE_TTL", "300"))

NEWS_LIST_KEY = "news:list"
NEWS_ITEM_KEY = "news:item:{id}"

async def list_news(db: AsyncSession, log) -> List[News]:
    r = await get_redis()

    cached = await r.get(NEWS_LIST_KEY)
    if cached:
        log.info("cache=hit source=news:list")
        data = json.loads(cached)
        # map -> DTO tùy bạn; hoặc trả thẳng data nếu API của bạn trả dict
        return data

    log.info("cache=miss source=news:list -> db")
    rows = (await db.execute(select(News).order_by(News.created_at.desc()))).scalars().all()
    data = [n.as_dict() for n in rows]   # tự viết as_dict hoặc schema Pydantic
    await r.setex(NEWS_LIST_KEY, NEWS_CACHE_TTL, json.dumps(data))
    return data

async def get_news(db: AsyncSession, news_id: int, log):
    r = await get_redis()
    key = NEWS_ITEM_KEY.format(id=news_id)
    cached = await r.get(key)
    if cached:
        log.info(f"cache=hit source=news:item id={news_id}")
        return json.loads(cached)

    log.info(f"cache=miss source=news:item id={news_id} -> db")
    obj = await db.get(News, news_id)
    if not obj:
        return None
    data = obj.as_dict()
    await r.setex(key, NEWS_CACHE_TTL, json.dumps(data))
    return data
