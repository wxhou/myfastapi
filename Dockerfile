FROM python:3.9

LABEL author="wxhou"

WORKDIR /myfastapi

COPY . .

ENV MY_WEBLOG_ENV=development

RUN pip install --no-cache-dir --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir poetry -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip config set install.trusted-host mirrors.aliyun.com
RUN poetry install
RUN pip install --no-cache-dir alembic -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN mkdir logs && mkdir upload

RUN python -m alembic revision --autogenerate -m "update"

RUN python -m alembic upgrade head

EXPOSE 8199

CMD gunicorn weblog:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8199