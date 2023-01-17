FROM python:3.9

LABEL author="wxhou"

WORKDIR /myfastapi

COPY . .

ENV MY_WEBLOG_ENV=development

RUN pip install --no-cache-dir --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir poetry -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN poetry install

SHELL ["/bin/bash", "-c"]

RUN mkdir logs && mkdir upload && mkdir -p alembic/versions

RUN poetry run alembic revision --autogenerate -m "update"

RUN poetry run alembic upgrade head

EXPOSE 8199

CMD poetry run gunicorn weblog:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8199