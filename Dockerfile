FROM python:3.9

LABEL author="wxhou"

WORKDIR /myfastapi

COPY . .

ENV MY_WEBLOG_ENV=development

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

SHELL ["/bin/bash", "-c"]

RUN mkdir logs && mkdir upload && mkdir -p alembic/versions

EXPOSE 8199

CMD gunicorn weblog:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8199