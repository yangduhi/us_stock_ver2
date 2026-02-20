import os
import redis.asyncio as redis
import json
from typing import Any, Optional

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


class RedisCache:
    def __init__(self):
        self.redis = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)

    async def get(self, key: str) -> Optional[Any]:
        try:
            val = await self.redis.get(key)
        except Exception:
            # Degrade gracefully when Redis is unavailable (e.g., local test runs).
            return None
        if val:
            try:
                return json.loads(val)
            except json.JSONDecodeError:
                return val
        return None

    async def set(self, key: str, value: Any, expire: int = 300):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        try:
            await self.redis.set(key, value, ex=expire)
        except Exception:
            # Cache write failure should not break API responses.
            return

    async def close(self):
        await self.redis.close()


cache = RedisCache()
