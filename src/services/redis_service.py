import hashlib
import json

from pydantic import BaseModel
from redis.asyncio import Redis

from core.config import settings
from pydantic import BaseModel
import backoff
from redis.exceptions import ConnectionError

from core.base_cache import CacheEngine


class RedisResponse(BaseModel):
    docs: list[dict]
    total: int = None


class RedisMixin:

    def __init__(self, cache_engine: CacheEngine, index: str):
        self.cache_engine = cache_engine
        self.index = index

    @backoff.on_exception(backoff.expo,
                          ConnectionError)
    async def get_from_redis(self, conditions: dict) -> RedisResponse:
        """Возвращает документы из Redis.

        :param conditions: параметры запроса
        :return: документы и общее количество документов
        """
        key = self._get_key(conditions)
        results = await self.cache_engine.get(key)
        if not results:
            return None
        return RedisResponse.parse_obj(json.loads(results))

    @backoff.on_exception(backoff.expo,
                          ConnectionError)
    async def put_to_redis(self, conditions: dict, docs: list, total: int | None = None) -> None:
        """Сохраняет документы и количество документов в Redis.

        :param conditions: условия
        :param docs: документы
        :param total: количество документов
        :return:
        """
        key = self._get_key(conditions)
        await self.cache_engine.set(
            key,
            RedisResponse(
                docs=docs,
                total=total,
            ).json(),
            settings.cache_lifetime,
        )

    def _get_key(self, conditions: dict) -> str:
        return (
            conditions['index'] if conditions['index'] else self.index
        ) + hashlib.md5(
            json.dumps(conditions).encode(),
        ).hexdigest()
