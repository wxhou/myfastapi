#!/bin/bash

uvicorn weblog:app --host 0.0.0.0 --port 8199 --reload &>/dev/null &

celery -A app.core.celery_app.celery worker -l info &>/dev/null &
