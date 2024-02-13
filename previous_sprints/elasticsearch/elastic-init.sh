#!/bin/bash
elasticdump --output http://elasticsearch_db:9200/movies --input indexes/movies.settings --type settings
elasticdump --output http://elasticsearch_db:9200/genres --input indexes/genres.settings --type settings
elasticdump --output http://elasticsearch_db:9200/persons --input indexes/persons.settings --type settings

elasticdump --output http://elasticsearch_db:9200/movies --input indexes/movies.mapping --type mapping
elasticdump --output http://elasticsearch_db:9200/genres --input indexes/genres.mapping --type mapping
elasticdump --output http://elasticsearch_db:9200/persons --input indexes/persons.mapping --type mapping

elasticdump --output http://elasticsearch_db:9200/movies --input data/movies.data --type data --limit 2000
elasticdump --output http://elasticsearch_db:9200/genres --input data/genres.data --type data --limit 2000
elasticdump --output http://elasticsearch_db:9200/persons --input data/persons.data --type data --limit 2000