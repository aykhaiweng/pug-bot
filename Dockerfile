FROM python:3.6-alpine

# Labels
LABEL maintainer="aykhaiweng@gmail.com"

ENV PYTHONBUFFERED 1

# Set up the working folder
WORKDIR /opt/pug-bot/
COPY . /opt/pug-bot/

# Update with gcc
RUN apk add --update --no-cache --virtual python3-dev gcc libc-dev

# Update PIP
RUN pip install -U pip
RUN pip install pipenv
RUN pipenv lock --requirements > /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

CMD ["./start.sh"]