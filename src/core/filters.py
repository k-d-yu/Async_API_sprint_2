from elasticsearch_dsl import Q, Search
from elasticsearch_dsl.query import Nested, QueryString, Term


def films_by_person(person: dict) -> dict:
    query = Search().filter(
        Nested(path='actors', query=Term(actors__id=person['id'])) |
        Nested(path='writers', query=Term(writers__id=person['id'])) |
        Nested(path='directors', query=Term(directors__id=person['id'])),
    )
    return query.to_dict()


def films_by_name(name: str) -> dict:
    query = Search().filter(
        Nested(path='actors', query=QueryString(query=name, fields=['actors.name']), inner_hits={}) |
        Nested(path='writers', query=QueryString(query=name, fields=['writers.name']), inner_hits={}) |
        Nested(path='directors', query=QueryString(query=name, fields=['directors.name']), inner_hits={}),
    )
    return query.to_dict()


def persons_by_query(query: str, fields: list):
    query = Search().filter(QueryString(query=query, fields=fields))
    return query.to_dict()


def films_by_title(search_title: str) -> dict:
    query = Search().query(Q("match", title={"query": search_title}))
    return query.to_dict()


def films_by_genre(search_genre: str) -> dict:
    query = Search().query(Q('nested', path='genres',
                             query=Q('match',
                                     genres__name={'query': search_genre.lower(), 'operator': 'and'})))
    return query.to_dict()
