import http
from typing import Callable

import pytest
from testdata.data import test_data
from testdata.es_mapping import MovieShort, PersonDetails


@pytest.mark.asyncio
async def test_get_person_by_id(
    make_get_request: Callable,
):
    response = await make_get_request(f'persons/{test_data.person_id}')

    assert response.status == http.HTTPStatus.OK, f'answer code is {response.status}, must be: {http.HTTPStatus.OK}'

    assert isinstance(response.body, dict), 'must be dict in response.body'

    assert PersonDetails(**response.body), 'wrong structure of response.body fields'


@pytest.mark.asyncio
async def test_get_persons_list(
    make_get_request: Callable,
):
    response = await make_get_request(f'persons/{test_data.person_id}/film')

    assert response.status == http.HTTPStatus.OK, f'answer code is {response.status}, must be: {http.HTTPStatus.OK}'

    assert isinstance(response.body['items'], list), 'must be list in response.body'

    assert len(response.body['items']) == 50, 'query must return list of 50 movies'

    assert MovieShort(**response.body['items'][0]), 'wrong structure of response.body element fields'


@pytest.mark.asyncio
async def test_person_not_found(
    make_get_request: Callable,
):
    response = await make_get_request(f'persons/{test_data.incorrect_id}')

    assert response.status == http.HTTPStatus.NOT_FOUND, f'response {response.status}, must be: {http.HTTPStatus.NOT_FOUND}'
