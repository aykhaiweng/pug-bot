############################################################
# Default build stage
############################################################
FROM python:3.9-alpine as base

LABEL maintainer="aykhaiweng@gmail.com"

ENV PYTHONBUFFERED 1

WORKDIR /opt/pugbot/
COPY . /opt/pugbot/
RUN apk add --update --virtual \
    python3-dev \
    gcc \
    libc-dev

RUN pip install -U pip
RUN pip install pipenv


############################################################
# Primary stage
############################################################
FROM base as primary
RUN pipenv lock --requirements > /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
ENTRYPOINT ["python3", "-m", "main.py"]


############################################################
# Dev stage
############################################################
FROM primary as dev
RUN pipenv lock --requirements --dev-only > /tmp/requirements-dev.txt
RUN pip install -r /tmp/requirements-dev.txt
ENTRYPOINT ["python3", "-m", "debugpy", "--listen", "0.0.0.0:5678", "main.py"]