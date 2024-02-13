import http
from typing import Callable

import pytest

from testdata.data import test_data
from testdata.es_mapping import GenreDetails, GenreShort


@pytest.mark.asyncio
async def test_get_genre_by_id(
    make_get_request: Callable,
):
    response = await make_get_request(f'genres/{test_data.genre_id}')

    assert response.status == http.HTTPStatus.OK, f'answer code is {response.status}, must be: {http.HTTPStatus.OK}'

    assert isinstance(response.body, dict), 'must be dict in response.body'

    assert GenreDetails(**response.body), 'wrong structure of response.body fields'


@pytest.mark.asyncio
async def test_get_genres_list(make_get_request):
    response = await make_get_request('genres', params={'page[size]': 50, 'page[number]': 1})

    assert response.status == http.HTTPStatus.OK, f'answer code is {response.status}, must be: {http.HTTPStatus.OK}'

    assert isinstance(response.body['items'], list), 'must be list in response.body'

    assert len(response.body['items']) == 50, 'query must return list of 100 genres'

    assert GenreShort(**response.body['items'][0]), 'wrong structure of response.body element fields'


@pytest.mark.asyncio
async def test_genre_not_found(make_get_request):
    response = await make_get_request(f'genres/{test_data.incorrect_id}')

    assert response.status == http.HTTPStatus.NOT_FOUND, f'response {response.status}, must be: {http.HTTPStatus.NOT_FOUND}'
