import pytest
import http

from typing import Callable
from tests.functional.testdata.redis_conditions import persons_condition, films_condition
from tests.functional.utils.redis_helper import RedisHelper

redis_helper = RedisHelper()


@pytest.mark.asyncio
async def test_persons_search_found(make_get_request: Callable):
    response = await make_get_request(f'persons', params={'full_name': 'Angela'})
    assert response.status == http.HTTPStatus.OK, 'Expected status: 200'
    assert len(response.body.get('items')) == 50, 'Expected count: 50'


@pytest.mark.asyncio
async def test_persons_search_not_found(make_get_request):
    response = await make_get_request(f'persons', params={'full_name': 'Sergei Burunov'})
    assert response.status == http.HTTPStatus.NOT_FOUND, 'Expected status: 404'


@pytest.mark.asyncio
async def test_persons_search_cache(make_get_request):
    response = await make_get_request(f'persons', params={'full_name': 'Henderson'})
    assert response.status == http.HTTPStatus.OK, 'Expected status: 200'
    conditions = persons_condition
    redis_response = await redis_helper.get_from_redis(conditions, index='movies')
    assert redis_response and redis_response.get('docs'), 'Expected documents in cache'


@pytest.mark.asyncio
async def test_film_search_found(make_get_request):
    response = await make_get_request(f'films', params={'search_title': 'high-level', 'page': 1})
    assert response.status == http.HTTPStatus.OK, 'Expected status: 200'
    assert response.body.get('total') == 564, 'Expected total: 564'


@pytest.mark.asyncio
async def test_film_search_not_found(make_get_request):
    response = await make_get_request(f'films', params={'search_title': 'not_found', 'page': 1})
    assert response.status == http.HTTPStatus.NOT_FOUND, 'Expected status: 404'


@pytest.mark.asyncio
async def test_films_search_cache(make_get_request):
    response = await make_get_request(f'films', params={'search_title': 'system', 'page': 1})
    assert response.status == http.HTTPStatus.OK, 'Expected status: 200'
    conditions = films_condition
    redis_response = await redis_helper.get_from_redis(conditions, index='movies')
    assert redis_response and redis_response.get('docs'), 'Expected documents in cache'


