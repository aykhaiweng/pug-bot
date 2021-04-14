FROM python:3.9-alpine

# Labels
LABEL maintainer="aykhaiweng@gmail.com"

ENV PYTHONBUFFERED 1

# Set up the working folder
WORKDIR /opt/pugbot/
COPY . /opt/pugbot/

# Update with gcc
RUN apk add --update --virtual python3-dev gcc libc-dev

# Update PIP
RUN pip install -U pip
RUN pip install pipenv
RUN pipenv lock --requirements > /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

CMD ["python3", "main.py"]