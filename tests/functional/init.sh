#!/bin/bash

cd utils
python3 wait_for_es.py
python3 wait_for_redis.py

pytest