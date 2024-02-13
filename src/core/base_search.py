from http import HTTPStatus
from uuid import UUID

from core.base_cache import CacheEngine
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import HTTPException

from core.config import settings
from core.misc import SCHEME
from services.redis_service import RedisMixin

import backoff
from elasticsearch.exceptions import ConnectionError as ElasticConnectionError
from redis.exceptions import ConnectionError as RedisConnectionError


class BaseSearch(RedisMixin):

    def __init__(self, cache_engine: CacheEngine, elastic: AsyncElasticsearch, type_of_response: SCHEME):
        super().__init__(cache_engine=cache_engine, index=type_of_response.index)
        self.elastic = elastic
        self.type_of_response = type_of_response

    def __post_init__(self):
        self.index = self.type_of_response.index

    def count_docs(self, list_of_docs) -> int:
        return len(list_of_docs)

    @backoff.on_exception(backoff.expo,
                          ElasticConnectionError)
    async def search_list_of_docs(self, query: dict | None = None):
        body = {'size': settings.max_window_size}
        if query:
            body['query'] = query['query']
        else:
            body['query'] = {'match_all': {}}
        redis_conditions: dict = {'query': query, 'index': self.index}
        try:
            redis_response = await self.get_from_redis(
                conditions=redis_conditions,
            )
            if redis_response:
                res: list[dict] = redis_response.docs
            else:
                data = await self.elastic.search(
                    index=self.index, body=body,
                )
                res = [document['_source'] for document in data['hits']['hits']]
        except NotFoundError:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
        await self.put_to_redis(
            conditions=redis_conditions,
            docs=res,
        )
        return [self.type_of_response(**rec) for rec in res]
    
    async def get_doc_by_id(self, doc_id: str):
        entity = await self._get_from_cache(doc_id)
        if not entity:
            entity = await self.get_doc_from_es(doc_id)
            if not entity:
                return None
            await self._put_film_to_cache(entity)
        return entity

    @backoff.on_exception(backoff.expo,
                          ElasticConnectionError)
    async def get_doc_from_es(self, doc_id: UUID):
        try:
            data = await self.elastic.get(self.index, doc_id)
        except NotFoundError:
            return None
        return self.type_of_response(**data['_source'])

    @backoff.on_exception(backoff.expo,
                          RedisConnectionError)
    async def _get_from_cache(self, entity_id: str):
        data = await self.cache_engine.get(str(entity_id))
        if not data:
            return None
        film = self.type_of_response.parse_raw(data)
        return film

    @backoff.on_exception(backoff.expo,
                          RedisConnectionError)
    async def _put_film_to_cache(self, entity: SCHEME):
        await self.cache_engine.set(entity.id, entity.json(), settings.cache_lifetime)
