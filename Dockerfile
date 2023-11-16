FROM python:3.9

LABEL author="wxhou"

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


WORKDIR /myfastapi

ENV MY_WEBLOG_ENV=development

COPY . .

SHELL ["/bin/bash", "-c"]

RUN mkdir logs && mkdir upload && mkdir -p alembic/versions

EXPOSE 8199

CMD gunicorn weblog:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8199