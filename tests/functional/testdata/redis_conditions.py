persons_condition = ('{"query": {"query": {"bool": {"filter": [{"bool": {"should": '
                     '[{"nested": {"path": "actors", "query": {"query_string": {"query": "Henderson", '
                     '"fields": ["actors.name"]}}, "inner_hits": {}}}, {"nested": {"path": "writers", '
                     '"query": {"query_string": {"query": "Henderson", "fields": ["writers.name"]}}, "inner_hits": {}}}, '
                     '{"nested": {"path": "directors", "query": {"query_string": {"query": "Henderson", "fields": '
                     '["directors.name"]}}, "inner_hits": {}}}]}}]}}}, "index": "movies"}')
films_condition = '{"query": {"query": {"match": {"title": {"query": "system"}}}}, "index": "movies"}'

