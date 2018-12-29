FROM python:3.6

ENV PY_DIR build/python/lib/python3.6/site-packages

RUN apt-get update
RUN apt-get install zip -y

RUN pip install awscli

COPY ./layer_package.sh .
ENTRYPOINT bash layer_package.sh
