.PHONY: clean kill run run2 all compose
.IGNORE: kill

# Makefile for building and pushing a Docker image
# Variables
include .env

all:
run:
	nohup ./env/bin/gunicorn weblog:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8199&

run2:
	nohup ./env/bin/gunicorn weblog:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8199 --reload >/dev/null 2>&1 &

compose:
	docker compose up --env-file .env --build -d

compose2:
	docker-compose up --env-file .env --build -d

# DB migration

dbinit:
	alembic init alembic

dbrevision:
	alembic revision --autogenerate -m "update"

dbupgrade:
	alembic upgrade head

dbdowngrade:
	alembic downgrade head


kill:
	pkill -f "weblog:app"

clean:
	@echo "clean is None"
