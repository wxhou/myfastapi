FROM python:3.9

LABEL author="wxhou"

WORKDIR /myfastapi

COPY . .

ENV MY_WEBLOG_ENV=development

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN chmod +x run.sh

RUN mkdir logs && mkdir upload

EXPOSE 8199

CMD uvicorn weblog:app --host 0.0.0.0 --port 8199 --reload