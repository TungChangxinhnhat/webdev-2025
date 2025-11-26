import json
from app.core.redis import get_redis

USER_KEY = "user:pub:{uid}"
USER_TTL = 600  # ví dụ 10 phút

async def cache_user_public(uid: int, data: dict):
    # data chỉ gồm fields công khai cần cho authorization (id, roles, is_active, ...)
    r = await get_redis()
    await r.setex(USER_KEY.format(uid=uid), USER_TTL, json.dumps(data))

async def get_user_public(uid: int) -> dict | None:
    r = await get_redis()
    raw = await r.get(USER_KEY.format(uid=uid))
    return json.loads(raw) if raw else None
