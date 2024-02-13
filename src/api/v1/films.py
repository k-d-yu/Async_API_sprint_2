from http import HTTPStatus

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, paginate

from core.filters import films_by_genre, films_by_title
from core.paginate import JSONAPIPage
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import FilmResponse, FilmsDetailsResponseModel
from models.genres import GenresResponseModel
from models.persons import PersonsResponseModel
from services.film import FilmSearch

router = APIRouter()


async def get_films_search(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmSearch:
    return FilmSearch(cache_engine=redis, elastic=elastic, type_of_response=FilmsDetailsResponseModel)


@router.get('/', response_model=Page[FilmResponse], summary='Поиск кинопроизведений',
            description='Предоставляется возможность сортировки кинопроизведений по убыванию (asc) или'
                        ' возрастанию (desc). Для этого необходимо выбрать поле для сортировки sort_by и '
                        'поле order. Также возможность поиска кинопроизведения по жанру и заголовку.',
            response_description='Название и рейтинг кинопроизведения', )
async def films_get_list_api(film_search: FilmSearch = Depends(get_films_search),
                             sort_by: str = Query(None, description='Поле для сортировки.',
                                                  regex='imdb_rating', enum=['imdb_rating']),
                             order: str = Query(None, description='Сортировка по убыванию (asc) или '
                                                                  'возрастанию (desc).',
                                                enum=['asc', 'desc']),
                             search_title: str = Query(None, description='Поиск по заголовку.'),
                             search_genre: str = Query(None, description='Поиск по жанру'),
                             ) -> JSONAPIPage[FilmResponse]:
    films = await film_search.search_list_of_docs()

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Кинопроизведения не найдены')

    if search_title:
        films = await film_search.search_list_of_docs(films_by_title(search_title))
        if not films:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Кинопроизведения не найдены')

    if search_genre:
        films = await film_search.search_list_of_docs(films_by_genre(search_genre))
        if not films:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Кинопроизведения не найдены')

    if sort_by:
        if sort_by not in FilmResponse.__annotations__:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                                detail=f'Некорректное поле сортировки: {sort_by}')
        films = sorted(films, key=lambda x: getattr(x, sort_by), reverse=(order == "desc"))
    return paginate(sequence=films, length_function=film_search.count_docs)


@router.get('/{film_id}',
            response_model=FilmsDetailsResponseModel,
            summary='Поиск кинопроизведения по ID.',
            description='Поиск кинопроизведения по ID.',
            response_description='Полная информация о кинопроизведение.', )
async def film_get_api(film_id: str,
                       film_search: FilmSearch = Depends(get_films_search),
                       ) -> FilmsDetailsResponseModel:
    film = await film_search.get_doc_by_id(doc_id=film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Кинопроизведение не найдено')
    genres_list: list[GenresResponseModel] = [GenresResponseModel(**genre.dict()) for genre in film.genres]
    actors_list: list[PersonsResponseModel] = [PersonsResponseModel(**actor.dict()) for actor in film.actors]
    writers_list: list[PersonsResponseModel] = [PersonsResponseModel(**writer.dict()) for writer in film.writers]
    directors_list: list[PersonsResponseModel] = [PersonsResponseModel(**director.dict())
                                                  for director in film.directors]
    return FilmsDetailsResponseModel(
        id=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        genres=genres_list,
        actors=actors_list,
        writers=writers_list,
        directors=directors_list,
    )
