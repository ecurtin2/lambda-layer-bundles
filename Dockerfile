FROM python:3.7

RUN apt-get update
RUN apt-get install zip -y

RUN pip install awscli

COPY ./layer_package.sh .
