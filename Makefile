.PHONY: clean kill run run2 all
.IGNORE: kill

all:
run:
	nohup ./env/bin/gunicorn weblog:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8199 --reload &

run2:
	nohup ./env/bin/gunicorn weblog:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8199 --reload >/dev/null 2>&1 &

kill:
	pkill -f "gunicorn weblog:app"

clean:
	@echo "clean is None"
