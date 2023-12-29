FROM python:3.9.5

LABEL author="wxhou"

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


WORKDIR /myfastapi

ARG my_weblog_env

ENV http_proxy=
ENV https_proxy=
ENV TZ=Asia/Shanghai
ENV MY_WEBLOG_ENV=${my_weblog_env}

COPY . .

RUN bash -c "if [ ! -d 'logs' ]; then mkdir logs; fi"