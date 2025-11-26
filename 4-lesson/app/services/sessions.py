import json, os
from datetime import timedelta
from app.core.redis import get_redis

SESSION_TTL = int(os.getenv("SESSION_TTL", "604800")) # 7d

SESSION_KEY = "sess:{sid}"

async def create_session(session_id: str, payload: dict):
    r = await get_redis()
    await r.setex(SESSION_KEY.format(sid=session_id), SESSION_TTL, json.dumps(payload))

async def get_session(session_id: str) -> dict | None:
    r = await get_redis()
    raw = await r.get(SESSION_KEY.format(sid=session_id))
    return json.loads(raw) if raw else None

async def delete_session(session_id: str):
    r = await get_redis()
    await r.delete(SESSION_KEY.format(sid=session_id))
