import http
import pytest

from urllib.parse import urlencode

from tests.functional.testdata.data import test_data
from tests.functional.testdata.es_mapping import MovieShort


@pytest.mark.asyncio
async def test_movie_existence(make_get_request):
    response = await make_get_request('films/' + test_data.movie_id)

    assert response.status == http.HTTPStatus.OK


@pytest.mark.asyncio
async def test_movie_existence_by_genre(make_get_request):
    params = {
        'search_genre': test_data.genre_title,
        'page': 1,
        'size': 50
    }
    response = await make_get_request('films/?' + urlencode(params))
    length = len([item['id'] for item in response.body['items']])

    assert response.status == http.HTTPStatus.OK
    assert length == 50
    assert [MovieShort(**item) for item in response.body['items']]


@pytest.mark.asyncio
async def test_imdb_rating_sort_asc(make_get_request):
    params = {
        'sort_by': 'imdb_rating',
        'order': 'asc',
        'page': 1,
        'size': 50
    }
    response = await make_get_request('films/?' + urlencode(params))
    imdb_ratings = [film['imdb_rating'] for film in response.body['items']]

    assert response.status == http.HTTPStatus.OK
    assert imdb_ratings == sorted(imdb_ratings)
    assert [MovieShort(**item) for item in response.body['items']]


@pytest.mark.asyncio
async def test_imdb_rating_sort_desc(make_get_request):
    params = {
        'sort_by': 'imdb_rating',
        'order': 'desc',
        'page': 1,
        'size': 50
    }
    response = await make_get_request('films/?' + urlencode(params))
    imdb_ratings = [film['imdb_rating'] for film in response.body['items']]

    assert response.status == http.HTTPStatus.OK
    assert imdb_ratings == sorted(imdb_ratings, reverse=True)
    assert [MovieShort(**item) for item in response.body['items']]
