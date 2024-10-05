FROM python:3.12

ENV PYTHONPATH /usr/src/vapecoin

RUN mkdir -p $PYTHONPATH
RUN mkdir -p $PYTHONPATH/static
RUN mkdir -p $PYTHONPATH/media

WORKDIR $PYTHONPATH

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Права на папки static и media
RUN chmod -R 755 /usr/src/vapecoin/static/
RUN chmod -R 755 /usr/src/vapecoin/media/

RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  libpq-dev \
  curl \
  ffmpeg

COPY . $PYTHONPATH
COPY ./req.txt $PYTHONPATH/

RUN pip install -r req.txt
