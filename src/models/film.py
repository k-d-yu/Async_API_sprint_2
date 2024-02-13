from typing import ClassVar

from models.base import BaseMixin
from models.genres import GenresResponseModel
from models.persons import PersonsResponseModel


class FilmsElasticModel(BaseMixin):
    _index: ClassVar[str] = 'movies'
    title: str
    description: str | None = None
    imdb_rating: float
    genres: list[dict[str, str]] | None = []
    actors: list[dict[str, str]] | None = []
    writers: list[dict[str, str]] | None = []
    directors: list[dict[str, str]] | None = []


class FilmResponse(BaseMixin):
    title: str
    imdb_rating: float
    index: ClassVar[str] = 'movies'


class FilmsDetailsResponseModel(FilmResponse):
    description: str | None = None
    genres: list[GenresResponseModel] | None = []
    actors: list[PersonsResponseModel] | None = []
    writers: list[PersonsResponseModel] | None = []
    directors: list[PersonsResponseModel] | None = []


class FilmRoles(FilmResponse):
    actors: list[PersonsResponseModel] | None = []
    writers: list[PersonsResponseModel] | None = []
    directors: list[PersonsResponseModel] | None = []
