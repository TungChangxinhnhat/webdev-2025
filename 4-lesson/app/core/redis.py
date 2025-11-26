# app/core/redis.py
from redis.asyncio import Redis
from contextlib import asynccontextmanager
import os

redis: Redis | None = None

@asynccontextmanager
async def lifespan(app):
    global redis
    redis = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"), decode_responses=True)
    try:
        yield
    finally:
        await redis.close()

async def cache_get(key): return await redis.get(key)
async def cache_set(key, value, ttl=300): return await redis.set(key, value, ex=ttl)
async def cache_del(key): return await redis.delete(key)
