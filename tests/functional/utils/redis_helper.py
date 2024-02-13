import hashlib
import json

from redis import Redis
from tests.functional.settings import settings


class RedisHelper:
    def __init__(self):
        self.redis = Redis(host=settings.redis_host, port=settings.redis_port)

    async def get_from_redis(self, conditions: str, index: str) -> dict | None:
        key = self._get_key(conditions, index)
        results = self.redis.get(key)
        if not results:
            return None
        return json.loads(results)

    def _get_key(self, conditions: str, index: str) -> str:
        return index + hashlib.md5(
            conditions.encode(),
        ).hexdigest()
