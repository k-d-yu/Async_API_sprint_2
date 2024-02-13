from pydantic import BaseModel


class BaseMixin(BaseModel):

    id: str


class GenreShort(BaseMixin):

    name: str


class MovieShort(BaseMixin):

    title: str
    imdb_rating: float


class GenreDetails(GenreShort):

    description: str


class PersonRole(BaseMixin):

    roles: list[str]


class PersonDetails(BaseMixin):

    full_name: str
    films: list[PersonRole]
