import pytest_asyncio
from aioredis import Redis, create_redis_pool

from typing import AsyncGenerator
from elasticsearch import AsyncElasticsearch

from tests.functional.settings import settings


@pytest_asyncio.fixture(scope='session')
async def elastic() -> AsyncGenerator[AsyncElasticsearch, None]:
    elastic = AsyncElasticsearch(
        hosts='{host}:{port}'.format(
            host=settings.elastic_host,
            port=settings.elastic_port,
        ),
    )
    try:
        yield elastic
    finally:
        await elastic.indices.delete('_all')
        await elastic.close()


@pytest_asyncio.fixture(scope='session')
async def redis() -> AsyncGenerator[Redis, None]:
    redis = await create_redis_pool(
        tuple(settings.redis_host, settings.redis_port), minsize=10, maxsize=20,
    )
    try:
        yield redis
    finally:
        await redis.flushall()
        redis.close()
        await redis.wait_closed()